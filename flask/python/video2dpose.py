import mediapipe as mp
import numpy as np
import cv2
import pyttsx3

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32
POSE_CONNECTIONS = [
    (NOSE, RIGHT_EYE_INNER),  # 0
    (RIGHT_EYE_INNER, RIGHT_EYE),
    (RIGHT_EYE, RIGHT_EYE_OUTER),
    (RIGHT_EYE_OUTER, RIGHT_EAR),
    (NOSE, LEFT_EYE_INNER),
    (LEFT_EYE_INNER, LEFT_EYE),
    (LEFT_EYE, LEFT_EYE_OUTER),
    (LEFT_EYE_OUTER, LEFT_EAR),
    (MOUTH_RIGHT, MOUTH_LEFT),
    (RIGHT_SHOULDER, LEFT_SHOULDER),
    (RIGHT_SHOULDER, RIGHT_ELBOW),  # 10
    (RIGHT_ELBOW, RIGHT_WRIST),  # 11
    (RIGHT_WRIST, RIGHT_PINKY),
    (RIGHT_WRIST, RIGHT_INDEX),
    (RIGHT_WRIST, RIGHT_THUMB),
    (RIGHT_PINKY, RIGHT_INDEX),
    (LEFT_SHOULDER, LEFT_ELBOW),  # 16
    (LEFT_ELBOW, LEFT_WRIST),  # 17
    (LEFT_WRIST, LEFT_PINKY),
    (LEFT_WRIST, LEFT_INDEX),
    (LEFT_WRIST, LEFT_THUMB),  # 20
    (LEFT_PINKY, LEFT_INDEX),
    (RIGHT_SHOULDER, RIGHT_HIP),  # 22
    (LEFT_SHOULDER, LEFT_HIP),  # 23
    (RIGHT_HIP, LEFT_HIP),
    (RIGHT_HIP, LEFT_HIP),
    (RIGHT_HIP, RIGHT_KNEE),
    (LEFT_HIP, LEFT_KNEE),
    (RIGHT_KNEE, RIGHT_ANKLE),
    (LEFT_KNEE, LEFT_ANKLE),
    (RIGHT_ANKLE, RIGHT_HEEL),  # 30
    (LEFT_ANKLE, LEFT_HEEL),
    (RIGHT_HEEL, RIGHT_FOOT_INDEX),
    (LEFT_HEEL, LEFT_FOOT_INDEX),
    (RIGHT_ANKLE, RIGHT_FOOT_INDEX),
    (LEFT_ANKLE, LEFT_FOOT_INDEX),
]

bone_idx_pairs = {'right-big-small-arm': (10, 11), 'left-big-small-arm': (16, 17), 'right-spin-big-arm': (22, 10),
                  'left-spin-big-arm': (16, 23)}


def gen_frames(input=1):
    def to_voice(string='this is a test'):
        engine = pyttsx3.init()
        engine.say(string)
        engine.runAndWait()

    to_voice()

    cap = cv2.VideoCapture(input)  # docker
    # cap = cv2.VideoCapture(0)  # local
    # cap.set(cv2.CAP_PROP_FPS, 15)

    analyzer = Analyzer()
    """TEST VOICE"""
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
                angles = get_bone_angle(xyzv, bone_idx_pairs=bone_idx_pairs, dim=2)
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

            # TODO: add analysis module and embed the tts engine in it
            # https://zhuanlan.zhihu.com/p/37923715
            # https://zhuanlan.zhihu.com/p/38136322
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

    def _get_all_bone_vecs(xyzv):
        all_bone_vecs = []
        for connection in POSE_CONNECTIONS:
            all_bone_vecs.append(_get_bone_vec(xyzv, start_idx=connection[0], end_idx=connection[1], dim=3))
        return all_bone_vecs

    def _cal_angle(x, y):
        cos_ = x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y)))
        return np.arccos(cos_) * 180 / np.pi

    res = dict()
    # ====
    conns = [(RIGHT_SHOULDER, RIGHT_ELBOW),  # RBigArm
             (RIGHT_WRIST, RIGHT_ELBOW),  # RSmallArm
             (LEFT_SHOULDER, LEFT_ELBOW),  # LBigArm
             (LEFT_WRIST, LEFT_ELBOW),  # LSmallArm
             (RIGHT_SHOULDER, RIGHT_HIP),  # RSpine
             (LEFT_SHOULDER, LEFT_HIP)]  # LSpine
    bones = [_get_bone_vec(xyzv, con[0], con[1]) for con in conns]
    bone_idx_pairs = {'right-big-small-arm': (0, 1), 'left-big-small-arm': (2, 3), 'right-spin-big-arm': (4, 0),
                      'left-spin-big-arm': (5, 2)}
    # ====
    for key, (bone1_idx, bone2_idx) in bone_idx_pairs.items():
        res[key] = _cal_angle(bones[bone1_idx], bones[bone2_idx])
    return res


class Analyzer():
    def analyze_pose(self, pose=None):
        self.pose = pose
        # TODO

    def to_voice(self, engine=None, string='this is a test'):
        engine = pyttsx3.init()
        engine.say(string)
        engine.runAndWait()
