import numpy as np

from configs.MediaPipe_joints import *

POSE_CONNECTIONS = [
    (NOSE, RIGHT_EYE_INNER),  # 0
    (RIGHT_EYE_INNER, RIGHT_EYE),  # 1
    (RIGHT_EYE, RIGHT_EYE_OUTER),  # 2
    (RIGHT_EYE_OUTER, RIGHT_EAR),  # 3
    (NOSE, LEFT_EYE_INNER),  # 4
    (LEFT_EYE_INNER, LEFT_EYE),  # 5
    (LEFT_EYE, LEFT_EYE_OUTER),  # 6
    (LEFT_EYE_OUTER, LEFT_EAR),  # 7
    (MOUTH_RIGHT, MOUTH_LEFT),  # 8

    (LEFT_SHOULDER, RIGHT_SHOULDER),  # 9
    # (RIGHT_SHOULDER, RIGHT_ELBOW),  # 10

    (RIGHT_ELBOW, RIGHT_SHOULDER),  # 10
    (RIGHT_ELBOW, RIGHT_WRIST),  # 11
    (RIGHT_WRIST, RIGHT_PINKY),  # 12
    (RIGHT_WRIST, RIGHT_INDEX),  # 13
    (RIGHT_WRIST, RIGHT_THUMB),  # 14
    (RIGHT_PINKY, RIGHT_INDEX),  # 15

    # (LEFT_SHOULDER, LEFT_ELBOW),  # 16
    (LEFT_ELBOW, LEFT_SHOULDER),  # 16

    (LEFT_ELBOW, LEFT_WRIST),  # 17
    (LEFT_WRIST, LEFT_PINKY),  # 18
    (LEFT_WRIST, LEFT_INDEX),  # 19
    (LEFT_WRIST, LEFT_THUMB),  # 20
    (LEFT_PINKY, LEFT_INDEX),  # 21

    # (RIGHT_SHOULDER, RIGHT_HIP),  # 22
    # (LEFT_SHOULDER, LEFT_HIP),  # 23
    (RIGHT_HIP, RIGHT_SHOULDER),  # 22
    (LEFT_HIP, LEFT_SHOULDER),  # 23

    (RIGHT_HIP, LEFT_HIP),  # 24
    (LEFT_HIP, RIGHT_HIP),  # 25
    (RIGHT_HIP, RIGHT_KNEE),  # 26
    (LEFT_HIP, LEFT_KNEE),  # 27
    # (RIGHT_KNEE, RIGHT_ANKLE),  # 28
    # (LEFT_KNEE, LEFT_ANKLE),  # 29
    (RIGHT_ANKLE, RIGHT_KNEE),  # 28
    (LEFT_ANKLE, LEFT_KNEE),  # 29

    (RIGHT_ANKLE, RIGHT_HEEL),  # 30
    (LEFT_ANKLE, LEFT_HEEL),  # 31
    (RIGHT_HEEL, RIGHT_FOOT_INDEX),  # 32
    (LEFT_HEEL, LEFT_FOOT_INDEX),  # 33
    (RIGHT_ANKLE, RIGHT_FOOT_INDEX),  # 34
    (LEFT_ANKLE, LEFT_FOOT_INDEX),  # 35
    #############################################
    (LEFT_WRIST, RIGHT_WRIST),  # 36
    (LEFT_KNEE, RIGHT_KNEE),  # 37
    (LEFT_ANKLE, RIGHT_ANKLE),  # 38
]

bone_idx_pairs_all = {'left-big-small-arm': (16, 17), 'right-big-small-arm': (10, 11),
                      'left-spin-big-arm': (16, 23), 'right-spin-big-arm': (10, 22),
                      'left-upper-lower-leg': (27, 29), 'right-upper-lower-leg': (26, 28),
                      'left-lower-leg-foot': (29, 33), 'right-lower-leg-foot': (28, 32),
                      'left-spin-upper-leg': (23, 27), 'right-spin-upper-leg': (22, 26),
                      }

_draw_idx = [9, 10, 11, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29]

# 从上到下
POSE_CONNECTIONS_DRAW = np.array(POSE_CONNECTIONS)[_draw_idx].tolist()

SHOW_POINT_IDX = [LEFT_ELBOW, RIGHT_ELBOW, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_KNEE, RIGHT_KNEE,
                  LEFT_HEEL, RIGHT_HEEL, LEFT_HIP, RIGHT_HIP, LEFT_WRIST, RIGHT_WRIST]

bone_idx_pairs = {'left-big-small-arm': (2, 3), 'right-big-small-arm': (0, 1),
                  'left-spin-big-arm': (5, 2), 'right-spin-big-arm': (4, 0),
                  'left-upper-lower-leg': (7, 9), 'right-upper-lower-leg': (6, 8),
                  'left-lower-leg-foot': (9, 11), 'right-lower-leg-foot': (8, 10),
                  'left-spin-upper-leg': (5, 7), 'right-spin-upper-leg': (4, 6),
                  }
draw_text_pos_joint = {
    'left-big-small-arm': LEFT_ELBOW, 'right-big-small-arm': RIGHT_ELBOW,
    'left-spin-big-arm': LEFT_SHOULDER, 'right-spin-big-arm': RIGHT_SHOULDER,
    'left-upper-lower-leg': LEFT_KNEE, 'right-upper-lower-leg': RIGHT_KNEE,
    'left-lower-leg-foot': LEFT_HEEL, 'right-lower-leg-foot': RIGHT_HEEL,
    'left-spin-upper-leg': LEFT_HIP, 'right-spin-upper-leg': RIGHT_HIP,
}
