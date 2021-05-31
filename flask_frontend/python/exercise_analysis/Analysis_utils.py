from video2dpose_utils import *
from video2dpose_utils import _get_bone_vec_mp, _cal_angle


def angle_in_range(angle, min_angle, max_angle):
    return min_angle < angle < max_angle


def isParallel(vec1, vec2):
    return angle_in_range(_cal_angle(vec1, vec2), 0, 20)


BONE_VEC_IDX_MP = {
    'shoulders': 9,
    'knees': 37,
    'ankles': 38,
    'wrists': 36,
    'hips': 25,
    'thighL': 27,
    'thighR': 26,
    'lowerLegL': 29,
    'lowerLegR': 28,
    'bigArmL': 16,
    'bigArmR': 10,
    'smallArmL': 17,
    'smallArmR': 11,
}


# NOTE: we don't have to calc spine-vec because we can check spin status
# by viewing whether shoulders parallel to knees and ankles

def _getSpineVec(depth_points):  # hip 中点到 shoulder 中点
    a = (np.array(depth_points[LEFT_SHOULDER]) + np.array(depth_points[RIGHT_SHOULDER])) / 2
    b = (np.array(depth_points[LEFT_HIP]) + np.array(depth_points[RIGHT_HIP])) / 2
    return b - a


def _getBoneVec(depth_points, boneName):
    return _get_bone_vec_mp(depth_points, POSE_CONNECTIONS[BONE_VEC_IDX_MP[boneName]][0],
                            POSE_CONNECTIONS[BONE_VEC_IDX_MP[boneName]][1], 3)


############ SQUAT ############
# 躯干与胫骨平行
def spineParallelLowerLeg(depth_points):
    SPINE_VEC = _getSpineVec(depth_points)
    LOWER_LEG_L = _getBoneVec(depth_points, 'lowerLegL')
    LOWER_LEG_R = _getBoneVec(depth_points, 'lowerLegR')
    return isParallel(SPINE_VEC, LOWER_LEG_L) or isParallel(SPINE_VEC, LOWER_LEG_R)


# 股骨位于水平面以下
def squatDownEnough(depth_points):
    LOWER_LEG_L = _getBoneVec(depth_points, 'lowerLegL')
    LOWER_LEG_R = _getBoneVec(depth_points, 'lowerLegR')
    THIGH_L = _getBoneVec(depth_points, 'thighL')
    THIGH_R = _getBoneVec(depth_points, 'thighR')
    return angle_in_range(_cal_angle(LOWER_LEG_L, THIGH_L), 40, 65) or \
           angle_in_range(_cal_angle(LOWER_LEG_R, THIGH_R), 40, 65)


# 双膝在双脚正上方
def kneesAboveFeet(depth_points):
    LOWER_LEG_L = _getBoneVec(depth_points, 'lowerLegL')
    LOWER_LEG_R = _getBoneVec(depth_points, 'lowerLegR')
    return angle_in_range(_cal_angle(LOWER_LEG_R, LOWER_LEG_L), 0, 20)


# 长杆与双脚平行(且长杆在双脚正上方)
def stickParallelFeet(depth_points):
    FEET = _getBoneVec(depth_points, 'ankles')
    STICK = _getBoneVec(depth_points, 'wrists')
    return angle_in_range(_cal_angle(FEET, STICK), 0, 20)


def scoreSquat(uvzv=None, depth_points=None):
    numTrues = spineParallelLowerLeg(depth_points) + kneesAboveFeet(depth_points) + kneesAboveFeet(depth_points) \
               + squatDownEnough(depth_points)
    if numTrues == 4:
        return 3
    elif numTrues == 3:
        return 2
    elif numTrues >= 0:
        return 1
    else:
        return 0


############ Hurdle ############
# 先判断哪只脚是抬腿脚
def isLeftLegHurdling(uvzv):  # check LEFT_ANKLE is higher than RIGHT_ANKLE in 2d
    return uvzv[LEFT_ANKLE][1] < uvzv[RIGHT_ANKLE][1]  # height is up-side-down in frames


# 抬腿高度到达杆子（站里腿膝盖高度）
def hurdleEnough(uvzv, leftLegHurdling):
    if leftLegHurdling:
        return uvzv[LEFT_ANKLE][1] < uvzv[RIGHT_KNEE][1]
    else:
        return uvzv[RIGHT_ANKLE][1] < uvzv[LEFT_KNEE][1]


# 髋膝踝均在矢状面上
def hipsKneesAnklesParallel(uvzv):
    HIPS = _getBoneVec(uvzv, 'hips')
    KNEES = _getBoneVec(uvzv, 'knees')
    ANKLES = _getBoneVec(uvzv, 'ankles')
    return (isParallel(HIPS, KNEES) + isParallel(KNEES, ANKLES) + isParallel(HIPS, ANKLES)) >= 2


# 身体高度不变
def standingStraight(uvzv):
    # 需要last frame的信息(?)
    return True


# 腰部无运动——hip 平行地面
def hipParallelFloor(depth_points):
    HIPS = _getBoneVec(depth_points, 'hips')
    ANKLES = _getBoneVec(depth_points, 'ankles')
    return isParallel(HIPS, ANKLES)


# 长杆与地面平行
def stickParallelFloor(depth_points):  # implementation same as stickParallelFeet
    FEET = _getBoneVec(depth_points, 'ankles')
    STICK = _getBoneVec(depth_points, 'wrists')
    return angle_in_range(_cal_angle(FEET, STICK), 0, 20)


def scoreHurdle(uvzv=None, depth_points=None):
    numTrues = hurdleEnough(uvzv, isLeftLegHurdling()) + hipsKneesAnklesParallel(uvzv) + hipParallelFloor(
        depth_points) + stickParallelFloor(depth_points)
    if not standingStraight(uvzv):
        return 1
    if numTrues == 4:
        return 3
    elif numTrues >= 0:
        return 2
    else:
        return 0


############ LegRaising ############
'''
# 先判断哪只脚是抬腿脚
def isLeftLegRaising(uvzv):  # check LEFT_ANKLE is higher than RIGHT_ANKLE in 2d
    return uvzv[LEFT_ANKLE][1] < uvzv[RIGHT_ANKLE][1]  # height is up-side-down in frames
'''


# 木杆位于大腿中点以上
def legRaiseEnough(uvzv, angle_min, angle_max):
    THIGH_L = _getBoneVec(uvzv, 'thighL')
    THIGH_R = _getBoneVec(uvzv, 'thighR')
    return angle_in_range(_cal_angle(THIGH_L, THIGH_R), angle_min, angle_max)


# 不弯腿
def legsStraight(uvzv):
    LOWER_LEG_L = _getBoneVec(uvzv, 'lowerLegL')
    LOWER_LEG_R = _getBoneVec(uvzv, 'lowerLegR')
    THIGH_L = _getBoneVec(uvzv, 'thighL')
    THIGH_R = _getBoneVec(uvzv, 'thighR')
    return angle_in_range(_cal_angle(LOWER_LEG_L, THIGH_L), 0, 15) or \
           angle_in_range(_cal_angle(LOWER_LEG_R, THIGH_R), 0, 15)


def scoreRaiseLeg(uvzv=None, depth_points=None):
    if not legsStraight(uvzv):
        return 0
    elif legRaiseEnough(uvzv, 75, 180):
        return 3
    elif legRaiseEnough(uvzv, 60, 75):
        return 2
    elif legRaiseEnough(uvzv, 0, 60):
        return 1
    else:
        return 0
