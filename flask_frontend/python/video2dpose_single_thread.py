import cv2
import mediapipe as mdp

from configs.MediaPipe_DrawConfig import *
from exercise_analysis import Analyzer

mp_drawing = mdp.solutions.drawing_utils
mp_pose = mdp.solutions.pose


def gen_frames(input_fid=0):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(input_fid)  # docker=1, local=0
    # cap.set(cv2.CAP_PROP_FPS, 15)

    """TEST VOICE"""
    analyzer = Analyzer()
    analyzer.to_voice(engine=None)

    frame_idx, text = 0, ''
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            results = pose.process(frame)
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # get 3d coords from mediapipe
            xyzv = []
            if results.pose_landmarks is not None:
                for landmark in results.pose_landmarks.landmark:
                    xyzv.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            frame_idx += 1
            if len(xyzv) and frame_idx % 15 == 0:
                # get bone angles
                angles = get_bone_angle(xyzv, bone_idx_pairs=bone_idx_pairs_all, dim=2)
                # print(angles)
                text, frame_idx = [key + ':' + str(int(value)) for key, value in angles.items()], 0
            # viz
            frame = cv2.flip(frame, 1)
            org = (10, 200)
            for t in text:
                cv2.putText(frame, t, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                org = (org[0], org[1] + 30)

            # analysis
            # num_landmarks = len(results.pose_landmarks.landmark)
            if frame_idx % 100 == 0:
                # analyzer.analyze_pose()
                analyzer.to_voice(engine=None, string="raise your arms higher")

            success, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def get_bone_angle(xyzv, bone_idx_pairs, dim=3):
    def _get_bone_vec(xyzv, start_idx, end_idx):
        return np.array(xyzv[end_idx * 4:end_idx * 4 + dim]) - np.array(xyzv[start_idx * 4:start_idx * 4 + dim])

    def _cal_angle(x, y):
        cos_ = x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y)))
        return np.arccos(cos_) * 180 / np.pi

    res = dict()
    bones = [_get_bone_vec(xyzv, con[0], con[1]) for con in POSE_CONNECTIONS]

    for key, (bone1_idx, bone2_idx) in bone_idx_pairs_all.items():
        res[key] = _cal_angle(bones[bone1_idx], bones[bone2_idx])
    return res
