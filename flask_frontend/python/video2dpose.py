import mediapipe as mdp
import pyttsx3
from .vid2pose_config import *
from exercise_analysis import Analyzer
from .video2dpose_utils import *
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time
import multiprocessing as mp
import tkinter as tk
import threading

VideoCapture = 0
using_realsense = os.path.exists('/dev/video2')
using_webcam = not using_realsense and os.path.exists('/dev/video0')

mp_drawing = mdp.solutions.drawing_utils
mp_pose = mdp.solutions.pose


class App(threading.Thread):
    """
    instance of this class can capture keyboard events in  a non-blocking way
    It is intend to track start and stop signals from the remote controller
    On Start and On Stop is the trigger for saving png images
    this is useful when aligning start-time between realsense and vicon
    and is also useful when the system is used by a patient, in which case the patient use it to indicate pain, shaking and calling-for-help
    """

    def __init__(self, state_dict=None):
        print("### Start listening to press event ###")
        # print('Now we can continue running code while mainloop runs!')
        threading.Thread.__init__(self)
        self.state_dict = state_dict
        self.fo = open("press.txt", "a")
        self.start()

    def onKeyPress(self, event=None):
        stime = str(time.time())
        print('%s\tYou pressed %s\n' % (stime, event.keycode,))
        self.fo.write(stime + '\n')
        self.fo.flush()

    def onPgDnPress(self, event):  # Stop Recording
        self.state_dict['isShowOnFlask'] = False
        print("stop saving pngs")
        self.onKeyPress(event)

    def onPgUpPress(self, event):  # Start Recording
        self.state_dict['isShowOnFlask'] = True
        print("start saving pngs")
        self.onKeyPress(event)

    def callback(self):
        self.fo.close()
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        # self.root.withdraw()
        self.root.iconify()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.bind("<Next>", self.onPgDnPress)  # Bind to PageDown
        self.root.bind("<Prior>", self.onPgUpPress)  # Bind to PageUp
        self.root.mainloop()


def get_image_rgb(color_img_q=None):
    cap = cv2.VideoCapture(VideoCapture)
    while True:
        success, color_image = cap.read()
        color_img_q.put(color_image)
        # print("color_img_q size: ", color_img_q.qsize())
        color_img_q.get() if color_img_q.qsize() > 1 else None


def get_image(color_img_q=None, depth_img_q=None):
    """
    this function is the main capturing process,
    it runs in a multiprocessing way as the opencv module gets the frames from realsense
    while the spawn of threads saves the frams as color and depth pngs
    """

    def _start():
        """
        this function runs at the begining of the video capturing process as it warms up the camera by letting go 100 frames (potentially) with fault
        """
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        profile = pipeline.start(config)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: ", depth_scale)

        align_to = rs.stream.color
        align = rs.align(align_to)
        # 获取图像，realsense刚启动的时候图像会有一些失真，我们保存第100帧图片。
        for i in range(100):
            data = pipeline.wait_for_frames()
            depth = data.get_depth_frame()
            color = data.get_color_frame()

        # 获取内参
        dprofile = depth.get_profile()
        cprofile = color.get_profile()

        cvsprofile = rs.video_stream_profile(cprofile)
        dvsprofile = rs.video_stream_profile(dprofile)

        color_intrin = cvsprofile.get_intrinsics()
        print("color_intrin", color_intrin)
        depth_intrin = dvsprofile.get_intrinsics()
        print("depth_intrin", depth_intrin)

        # 外参
        extrin = dprofile.get_extrinsics_to(cprofile)
        print("extrin", extrin)
        return pipeline, align

    pipeline, align = _start()
    while True:
        data = pipeline.wait_for_frames()

        color = data.get_color_frame()
        color_image = np.asanyarray(color.get_data())

        depth = data.get_depth_frame()
        depth_image = np.asanyarray(depth.get_data())

        # color_image = cv2.flip(color_image, -1)
        color_img_q.put(color_image)
        # print("color_img_q size: ", color_img_q.qsize())
        color_img_q.get() if color_img_q.qsize() > 1 else None

        # depth_image = cv2.flip(depth_image, -1)
        depth_img_q.put(depth_image)
        # print("color_img_q size: ", color_img_q.qsize())
        depth_img_q.get() if depth_img_q.qsize() > 1 else None


def apply_2d_inference_model(color_img_q, pose_2d_img_q, xyzv_q, my_gpu_memory_limit):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    while True:
        while color_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = origin_img = color_img_q.get()  # one tf model
        # print("color_img_q.get()", frame.shape)

        '''inference'''
        results = pose.process(frame)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pose_2d_img_q.put(frame)
        # print("pose_2d_img_q size: ", pose_2d_img_q.qsize())
        pose_2d_img_q.get() if pose_2d_img_q.qsize() > 3 else None

        # get 3d coords from mediapipe
        xyzv = []
        if results.pose_landmarks is not None:
            [xyzv.extend([lm.x, lm.y, lm.z, lm.visibility]) for lm in results.pose_landmarks.landmark]
        xyzv_q.put(xyzv)
        xyzv_q.get() if xyzv_q.qsize() > 3 else None


def getRealsenseMappedDepth(DepthImageAligned, jointXYZVs=np.zeros(132)):
    # TODO Assert
    if len(jointXYZVs) != 132:
        return np.zeros(33)
    return np.array([DepthImageAligned[x][y] for x, y in np.array(jointXYZVs).reshape(33, 4)])


def apply_lifting_model(depth_img_q, pose_2d_img_q, result_img_q, xyzv_q, my_gpu_memory_limit):
    while True:
        # timer = time.time()
        # gpu_limit_rate = my_gpu_memory_limit / int(os.popen('nvidia-smi').readlines()[8].split('/')[2].split('MiB')[0])
        # '''loading model'''
        # ckpt_pwd = os.path.join(model_path, 'frozen_inference_graph.pb')
        # print("||| Loading model time:", time.time() - timer)

        while pose_2d_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = pose_2d_img = pose_2d_img_q.get()
        # print("pose_2d_img_q.get()", frame.shape)

        '''inference'''
        while xyzv_q.qsize() == 0:
            time.sleep(0.01)
        xyzv = xyzv_q.get()
        # print("xyzv_q.get()", xyzv)

        ####################################################################################
        # TODO 可以考虑把 xyzv和depth放在同一个queue
        while depth_img_q.qsize() == 0:
            time.sleep(0.01)
        depth_img = depth_img_q.get()
        z_rs = getRealsenseMappedDepth(depth_img, xyzv)

        # TODO merge the depths
        ####################################################################################

        if len(xyzv):
            angles = get_bone_angle(xyzv, bone_idx_pairs=bone_idx_pairs, dim=2)
            text, frame_idx = [key + ':' + str(int(value)) for key, value in angles.items()], 0
            frame, position = cv2.flip(frame, 1), (10, 200)
            for t in text:
                cv2.putText(frame, t, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                position = (position[0], position[1] + 30)
        result_img_q.put(frame)
        # print("result_img_q size: ", result_img_q.qsize())
        result_img_q.get() if result_img_q.qsize() > 7 else None


def run():
    if not using_webcam and not using_realsense:
        exit("NO Camera")
    mp.set_start_method(method='spawn')
    with mp.Manager() as manager:
        state_dict = manager.dict()
        state_dict['isShowOnFlask'] = False

        app = App(state_dict)
        color_img_q = mp.Queue(maxsize=2)
        depth_img_q = mp.Queue(maxsize=2)
        pose_2d_img_q = mp.Queue(maxsize=4)
        xyzv_q = mp.Queue(maxsize=4)
        result_img_q = mp.Queue(maxsize=8)

        if using_realsense:
            processes = [
                mp.Process(target=get_image, args=(color_img_q, depth_img_q)),
                mp.Process(target=apply_2d_inference_model,
                           args=(color_img_q, pose_2d_img_q, xyzv_q, my_gpu_memory_limit)),
                mp.Process(target=apply_lifting_model,
                           args=(depth_img_q, pose_2d_img_q, result_img_q, xyzv_q, my_gpu_memory_limit)),
            ]
        elif using_webcam:
            processes = [
                mp.Process(target=get_image_rgb, args=(color_img_q,)),
                mp.Process(target=apply_2d_inference_model,
                           args=(color_img_q, pose_2d_img_q, xyzv_q, my_gpu_memory_limit)),
                mp.Process(target=apply_lifting_model, args=(pose_2d_img_q, result_img_q, xyzv_q, my_gpu_memory_limit)),
            ]

        [setattr(process, "daemon", True) for process in processes]
        [process.start() for process in processes]
        while True:
            while result_img_q.qsize() == 0:
                time.sleep(0.005)

            frame = result_img_q.get()
            success, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            if state_dict['isShowOnFlask']:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

        # print("### END ###")
        # [process.join() for process in processes]
