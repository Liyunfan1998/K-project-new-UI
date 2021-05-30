import mediapipe as mdp
import pyttsx3

from configs.MediaPipe_DrawConfig import *

# from exercise_analysis import Analyzer
from .video2dpose_utils import *
import pyrealsense2 as rs
import numpy as np
import cv2
import os, sys
import time
import multiprocessing as mp
import argparse

SAVE_AS_PNG = False
VideoCapture = '/home/liyunfan/Desktop/GraduationProject/K-project-new-UI/flask_frontend/tools/collect_04212021_18_07_25.avi'
# VideoCapture = 0
using_realsense = os.path.exists('/dev/video2')
using_webcam = not using_realsense and os.path.exists('/dev/video0')
using_video = VideoCapture != 0

sys.path.append('/usr/local/python')
from openpose import pyopenpose as op

"""
poseModel = op.PoseModel.BODY_25
print(op.getPoseBodyPartMapping(poseModel))
print(op.getPoseNumberBodyParts(poseModel))
print(op.getPosePartPairs(poseModel))
print(op.getPoseMapIndex(poseModel))
"""


class RawImgStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(VideoCapture)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

    def get(self):
        success, color_image = self.cap.read()
        return cv2.flip(color_image, 1)  # flip on capture


class RealsenseStream:
    def __init__(self):
        self.pipeline = rs.pipeline()
        rs.config().enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) \
            .enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.align = rs.align(rs.stream.color)
        for i in range(100):  # 获取图像，realsense刚启动的时候图像会有一些失真，我们保存第100帧图片。
            self.pipeline.wait_for_frames()

    def get(self):
        data = self.pipeline.wait_for_frames()
        color = data.get_color_frame()
        color_image = np.asanyarray(color.get_data())
        depth = data.get_depth_frame()
        depth_image = np.asanyarray(depth.get_data())
        return color_image, depth_image


def apply_depth_mapping(depth_img_q, pose_2d_img_q, result_img_q, xyv_q):
    while True:
        while xyv_q.qsize() == 0:
            time.sleep(0.01)
        xyv = xyv_q.get()
        # print("xyzv_q.get()", xyzv)

        if depth_img_q is not None:
            while depth_img_q.qsize() == 0:
                time.sleep(0.01)
            depth_img = depth_img_q.get()


def apply_lifting_model(pose_2d_img_q, result_img_q, xyv_q, my_gpu_memory_limit=0):
    while True:
        # timer = time.time()
        # gpu_limit_rate = my_gpu_memory_limit / int(os.popen('nvidia-smi').readlines()[8].split('/')[2].split('MiB')[0])
        # '''loading model'''
        # ckpt_pwd = os.path.join(model_path, 'frozen_inference_graph.pb')
        # print("||| Loading model time:", time.time() - timer)

        '''inference'''
        while xyv_q.qsize() == 0:
            time.sleep(0.01)
        xyv = xyv_q.get()
        # print("xyzv_q.get()", xyzv)


def run():
    if not using_webcam and not using_realsense and not using_video:
        exit("NO INPUT")

    opWrapper = op.WrapperPython()
    params = dict()
    params["model_folder"] = "/usr/local/python/openpose/models/"
    # opWrapper = op.WrapperPython(op.ThreadManagerMode.Synchronous)
    opWrapper.configure(params)
    opWrapper.start()
    idx_coco_in_b25 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    rawImgStream = RawImgStream()

    frame_cnt, start = 0, time.time()
    while True:
        frame_cnt += 1
        color_img = rawImgStream.get()
        datum = op.Datum()
        datum.cvInputData = color_img
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        if datum.poseKeypoints is None: break
        # print("Body keypoints:", str(datum.poseKeypoints.shape))
        xyv = datum.poseKeypoints[0]
        x, y = xyv[:, 0], xyv[:, 1]
        # for sk in conns_op:
        #     cv2.line(color_img, (x[sk[0]], y[sk[0]]), (x[sk[1]], y[sk[1]]), color=(0, 255, 0), thickness=2)
        # for i in idx_coco_in_b25:
        #     cv2.circle(color_img, (x[i], y[i]), radius=2, color=(0, 0, 255), thickness=2)

        if SAVE_AS_PNG:
            save_dir = './tmp/'
            cv2.imwrite(save_dir + 'color' + str(time.time()) + '.png', color_img)

        success, buffer = cv2.imencode('.jpg', datum.cvOutputData)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')  # concat frame one by one and show result

    print(frame_cnt / (time.time() - start))
