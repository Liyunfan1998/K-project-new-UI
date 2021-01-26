import mediapipe as mp
import  numpy as np
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
import cv2
from Tools.pose_baseline_mediapipe import Lifter

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
while cap.isOpened():
    ret, image = cap.read()
    results = pose.process(image)
    lifter = Lifter(base='./')
    xyzv = []
    if results.pose_landmarks is not None:
        for landmark in results.pose_landmarks.landmark:
            xyzv.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
        poses3d = lifter.get_3d_joints(xyzv)
        print(np.array(poses3d).shape)

cap.release()
pose.release()
