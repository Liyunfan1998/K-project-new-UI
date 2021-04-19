import os
import time
import mediapipe as mdp
import numpy as np
import cv2
import pyttsx3
import multiprocessing as mp
from .vid2pose_config import *
from exercise_analysis import Analyzer
from .video2dpose_utils import *

mp_drawing = mdp.solutions.drawing_utils
mp_pose = mdp.solutions.pose


def queue_img_put(q_put, VideoCapture=0):
    cap = cv2.VideoCapture(VideoCapture)
    while True:
        success, frame = cap.read()
        q_put.put(frame) if success else None
        # print("origin_img_q size: ", q_put.qsize())
        q_put.get() if q_put.qsize() > 1 else None


'''def queue_img_get(q_get):
    cv2.namedWindow("XY", flags=cv2.WINDOW_FREERATIO)
    # timer, time1 = time.time(), time.time()
    while True:
        while q_get.qsize() == 0:
            time.sleep(0.01)
        frame = q_get.get()
        print("# get and render")
        # timer, time1 = time1, time.time()
        (cv2.imshow("XY", frame), cv2.waitKey(1))'''


def apply_2d_inference_model(origin_img_q, pose_2d_img_q, xyzv_q, my_gpu_memory_limit):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    while True:
        while origin_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = origin_img = origin_img_q.get()  # one tf model
        print("origin_img_q.get()", frame.shape)

        '''inference'''
        results = pose.process(frame)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pose_2d_img_q.put(frame)
        print("pose_2d_img_q size: ", pose_2d_img_q.qsize())
        pose_2d_img_q.get() if pose_2d_img_q.qsize() > 3 else None

        # get 3d coords from mediapipe
        xyzv = []
        if results.pose_landmarks is not None:
            [xyzv.extend([lm.x, lm.y, lm.z, lm.visibility]) for lm in results.pose_landmarks.landmark]
        xyzv_q.put(xyzv)
        xyzv_q.get() if xyzv_q.qsize() > 3 else None


def apply_lifting_model(pose_2d_img_q, result_img_q, xyzv_q, my_gpu_memory_limit):
    while True:
        # timer = time.time()
        # gpu_limit_rate = my_gpu_memory_limit / int(os.popen('nvidia-smi').readlines()[8].split('/')[2].split('MiB')[0])
        # '''loading model'''
        # ckpt_pwd = os.path.join(model_path, 'frozen_inference_graph.pb')
        # print("||| Loading model time:", time.time() - timer)

        while pose_2d_img_q.qsize() == 0:
            time.sleep(0.01)
        frame = pose_2d_img = pose_2d_img_q.get()
        print("pose_2d_img_q.get()", frame.shape)

        '''inference'''
        while xyzv_q.qsize() == 0:
            time.sleep(0.01)
        xyzv = xyzv_q.get()
        # print("xyzv_q.get()", xyzv)

        if len(xyzv):
            angles = get_bone_angle(xyzv, bone_idx_pairs=bone_idx_pairs, dim=2)
            text, frame_idx = [key + ':' + str(int(value)) for key, value in angles.items()], 0
            frame, position = cv2.flip(frame, 1), (10, 200)
            for t in text:
                cv2.putText(frame, t, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                position = (position[0], position[1] + 30)
        result_img_q.put(frame)
        print("result_img_q size: ", result_img_q.qsize())
        result_img_q.get() if result_img_q.qsize() > 7 else None


def run():
    mp.set_start_method(method='spawn')

    origin_img_q = mp.Queue(maxsize=2)
    pose_2d_img_q = mp.Queue(maxsize=4)
    xyzv_q = mp.Queue(maxsize=4)
    result_img_q = mp.Queue(maxsize=8)

    processes = [
        mp.Process(target=queue_img_put, args=(origin_img_q,)),
        mp.Process(target=apply_2d_inference_model, args=(origin_img_q, pose_2d_img_q, xyzv_q, my_gpu_memory_limit)),
        mp.Process(target=apply_lifting_model, args=(pose_2d_img_q, result_img_q, xyzv_q, my_gpu_memory_limit)),
        # mp.Process(target=queue_img_get, args=(result_img_q,)),
    ]

    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    while True:
        while result_img_q.qsize() == 0:
            time.sleep(0.005)

        frame = result_img_q.get()
        success, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    # print("### END ###")
    # [process.join() for process in processes]
