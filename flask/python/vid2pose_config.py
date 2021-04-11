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

model_path = ""
my_gpu_memory_limit = ""

org = (10, 200)

conns = [(RIGHT_SHOULDER, RIGHT_ELBOW),  # RBigArm
         (RIGHT_WRIST, RIGHT_ELBOW),  # RSmallArm
         (LEFT_SHOULDER, LEFT_ELBOW),  # LBigArm
         (LEFT_WRIST, LEFT_ELBOW),  # LSmallArm
         (RIGHT_SHOULDER, RIGHT_HIP),  # RSpine
         (LEFT_SHOULDER, LEFT_HIP)]  # LSpine

bone_idx_pairs = {'right-big-small-arm': (0, 1), 'left-big-small-arm': (2, 3), 'right-spin-big-arm': (4, 0),
                  'left-spin-big-arm': (5, 2)}
