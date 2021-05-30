import multiprocessing as mp
import os

import cv2
import mediapipe as mdp

from .video2dpose_utils import *

SAVE_AS_PNG = False
VideoCapture = '/home/liyunfan/Desktop/GraduationProject/K-project-new-UI/flask_frontend/tools/collect_04212021_18_07_25.avi'
# VideoCapture = 0
using_realsense = os.path.exists('/dev/video2')
using_webcam = not using_realsense and os.path.exists('/dev/video0')
using_video = VideoCapture != 0
mp_drawing = mdp.solutions.drawing_utils
mp_pose = mdp.solutions.pose


def get_image_rgb(color_img_q=None):
    cap = cv2.VideoCapture(VideoCapture)
    while True:
        success, color_image = cap.read()
        color_image = cv2.flip(color_image, 1)  # flip on capture
        time.sleep(0.03)
        color_img_q.put(color_image)
        color_img_q.get() if color_img_q.qsize() > 1 else None


def get_image_toCameraSpace_Show(color_img_q=None, uvzv_q=None, pose_2d_img_q=None, result_img_q=None):
    """
    this function is the main capturing process,
    it runs in a multiprocessing way as the opencv module gets the frames from realsense
    while the spawn of threads saves the frams as color and depth pngs
    """

    def _start_rs():
        """
        this function runs at the begining of the video capturing process as it warms up the camera by letting go 100 frames (potentially) with fault
        """
        # Configure depth and color streams
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        profile = pipeline.start(config)
        # depth_sensor = profile.get_device().first_depth_sensor()
        # depth_scale = depth_sensor.get_depth_scale()
        # print("Depth Scale is: ", depth_scale)
        align_to = rs.stream.color
        align = rs.align(align_to)
        # 获取图像，realsense刚启动的时候图像会有一些失真，我们保存第100帧图片。
        # for i in range(100):
        #     data = pipeline.wait_for_frames()
        #     data = align.process(data)
        #     depth = data.get_depth_frame()
        #     color = data.get_color_frame()
        #
        # # 获取内参
        # dprofile = depth.get_profile()
        # cprofile = color.get_profile()
        #
        # cvsprofile = rs.video_stream_profile(cprofile)
        # dvsprofile = rs.video_stream_profile(dprofile)
        #
        # color_intrin = cvsprofile.get_intrinsics()
        # print("color_intrin", color_intrin)
        # depth_intrin = dvsprofile.get_intrinsics()
        # print("depth_intrin", depth_intrin)
        #
        # # 外参
        # extrin = dprofile.get_extrinsics_to(cprofile)
        # print("extrin", extrin)
        return pipeline, align

    pipeline, align = _start_rs()
    while True:
        data = pipeline.wait_for_frames()
        data = align.process(data)
        color = data.get_color_frame()
        color_image = np.asanyarray(color.get_data())  # assert color_image.shape == (480, 640, 3)
        depth = data.get_depth_frame()  # assert depth_image.shape == (480, 640)
        depth_image = np.asanyarray(depth.get_data())
        color_img_q.put(color_image)
        color_img_q.get() if color_img_q.qsize() > 1 else None
        depth_intrin = depth.profile.as_video_stream_profile().intrinsics

        assert depth_intrin is not None

        while uvzv_q.qsize() == 0:
            time.sleep(0.01)
        uvzv = uvzv_q.get()

        while pose_2d_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = pose_2d_img_q.get()

        if np.any(uvzv):  # not all zeros
            depth_points = np.array(getCameraSpacePointCoords(uvzv, depth_intrin, depth))
            pos_angle_dict = show_angle_on_joints(uvzv, depth_points, dim=3)
            uvzv = uvzv.astype(int)
            camera_point_text = [
                ("({:.1f},{:.1f},{:.1f})".format(depth_points[i][0], depth_points[i][1], depth_points[i][2]),
                 (uvzv[i][0], uvzv[i][1])) for i in SHOW_POINT_IDX]
            angle_text = [("{:.0f}".format(angle), pos) for angle_name, (pos, angle) in pos_angle_dict.items()]
            [cv2.putText(frame, t, (position[0] + 5, position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                         (255, 255, 255), 2, cv2.LINE_AA) for t, position in angle_text]
            [cv2.putText(frame, t, (position[0], position[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                         (255, 0, 0), 1, cv2.LINE_AA) for t, position in camera_point_text]
            [cv2.putText(frame, str((position[0], position[1])), (position[0], position[1] - 10),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.2,
                         (0, 255, 255), 1, cv2.LINE_AA) for t, position in camera_point_text]

        result_img_q.put(frame)
        result_img_q.get() if result_img_q.qsize() > 7 else None


def apply_2d_inference_model(color_img_q, pose_2d_img_q, uvzv_q, my_gpu_memory_limit=0):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    while True:
        while color_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = color_img_q.get()
        if frame is not None:
            results = pose.process(frame)
            if results is None or results.pose_landmarks is None:
                uvzv_q.put(np.zeros((33, 4)))
                uvzv_q.get() if uvzv_q.qsize() > 3 else None
                pose_2d_img_q.put(frame)
                pose_2d_img_q.get() if pose_2d_img_q.qsize() > 3 else None
            else:
                # put uvzv first for next process in line
                uvzv = np.array(
                    [[min(lm.x * 640.0, 640 - 1), min(lm.y * 480.0, 480 - 1), lm.z * 640.0, lm.visibility] for lm in
                     results.pose_landmarks.landmark])
                uvzv_q.put(np.absolute(uvzv))
                uvzv_q.get() if uvzv_q.qsize() > 3 else None
                # draw skeleton later
                if frame is not None and results.pose_landmarks is not None:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, POSE_CONNECTIONS_DRAW)
                pose_2d_img_q.put(frame)
                pose_2d_img_q.get() if pose_2d_img_q.qsize() > 3 else None


def apply_lifting_model(depth_img_q, pose_2d_img_q, result_img_q, uvzv_q, my_gpu_memory_limit=0):
    while True:
        # timer = time.time()
        # gpu_limit_rate = my_gpu_memory_limit / int(os.popen('nvidia-smi').readlines()[8].split('/')[2].split('MiB')[0])
        # '''loading model'''
        # ckpt_pwd = os.path.join(model_path, 'frozen_inference_graph.pb')
        # print("||| Loading model time:", time.time() - timer)

        while pose_2d_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = pose_2d_img_q.get()

        while uvzv_q.qsize() == 0:
            time.sleep(0.01)
        uvzv = uvzv_q.get()

        if len(uvzv):
            pos_angle_dict = show_angle_on_joints(uvzv, None, dim=2)
            text, frame_idx = [(str(int(angle)), pos) for angle_name, (pos, angle) in
                               pos_angle_dict.items()], 0  # angle_name + ':' + str(int(angle))
            for t, position in text:
                cv2.putText(frame, t, (position[0] + 5, position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2, cv2.LINE_AA)
        result_img_q.put(frame)
        result_img_q.get() if result_img_q.qsize() > 7 else None


def run():
    if not using_webcam and not using_realsense and not using_video:
        exit("NO Camera")
    try:
        mp.set_start_method(method='spawn')
    except RuntimeError:
        pass
    with mp.Manager() as manager:
        state_dict = manager.dict()
        state_dict['isShowOnFlask'] = True
        # app = App(state_dict)
        color_img_q = mp.Queue(maxsize=2)
        xyz_q = mp.Queue(maxsize=4)
        pose_2d_img_q = mp.Queue(maxsize=4)
        uvzv_q = mp.Queue(maxsize=4)
        result_img_q = mp.Queue(maxsize=8)

        if using_realsense:
            processes = [
                mp.Process(target=get_image_toCameraSpace_Show,
                           args=(color_img_q, uvzv_q, pose_2d_img_q, result_img_q)),
                mp.Process(target=apply_2d_inference_model,
                           args=(color_img_q, pose_2d_img_q, uvzv_q, 0)),
            ]
        else:  # webcam and video
            processes = [
                mp.Process(target=get_image_rgb, args=(color_img_q,)),
                mp.Process(target=apply_2d_inference_model,
                           args=(color_img_q, pose_2d_img_q, uvzv_q, 0)),
                mp.Process(target=apply_lifting_model,
                           args=(None, pose_2d_img_q, result_img_q, uvzv_q, 0)),
            ]

        [setattr(process, "daemon", True) for process in processes]
        [process.start() for process in processes]
        frame_cnt, start = 0, time.time()
        while True:
            while result_img_q.qsize() == 0:
                time.sleep(0.005)

            frame = result_img_q.get()
            if frame is None: break
            frame_cnt += 1

            if SAVE_AS_PNG:
                save_dir = './tmp/'
                cv2.imwrite(save_dir + 'color' + str(time.time()) + '.png', frame)

            success, buffer = cv2.imencode('.jpg', frame)
            if state_dict['isShowOnFlask']:
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
        print(frame_cnt / (time.time() - start))
