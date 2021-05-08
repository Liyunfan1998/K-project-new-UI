import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
import cv2
# from Tools.pose_baseline_mediapipe import Lifter
from pandas import DataFrame

vid_path = '/home/liyunfan/Desktop/GraduationProject/K-project-new-UI/flask_frontend/tools/collect_0428/output.mp4'
cap = cv2.VideoCapture(vid_path)
# cap.set(cv2.CAP_PROP_FPS, 10)
all_xyzv = []

while cap.isOpened():
    ret, image = cap.read()
    try:
        results = pose.process(image)
        # lifter = Lifter(base='./')
        xyzv = []
        if results.pose_landmarks is not None:
            for landmark in results.pose_landmarks.landmark:
                xyzv.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            print(len(xyzv))
            # poses3d = lifter.get_3d_joints(xyzv)
            # print(np.array(poses3d).shape)
        else:
            xyzv = [0] * 132
        all_xyzv.append(xyzv)
    except:
        DataFrame(np.matrix(all_xyzv)).to_csv(vid_path + '.csv')
        break

cap.release()
# pose.release()
