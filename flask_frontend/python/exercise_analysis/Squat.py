from .Analysis_utils import *


def squat(left_knee_angle_from_front, right_knee_angle_from_front, dist_hip_to_foot, dist_knee_to_foot, dist_hip_to_hip,
          using_support_pad=False):
    '''
    analyze the squat motion and give instructions to patients
    :param left_knee_angle_from_front: viewed form front camera, the angle of the patient's between the upper and lower left legs
    :param right_knee_angle_from_front: viewed form front camera, the angle of the patient's between the upper and lower right legs
    :param squat_depth_ratio: the division of hip-to-foot distance and hip-to-hip distance,  hip_to_foot_dist/hip_to_hip_dist
    y_hip = (y_left_hip + y_right_hip)/2
    y_foot = (y_left_foot + y_right_foot)/2
    hip_to_foot_dist = y_hip - y_foot
    hip_to_hip_dist = abs(x_left_hip - x_right_hip)
    :return: list of strings, which are instructions for the patient, to be turned to voice messages by pyttsx3 engine
    '''

    squat_depth_ratio = dist_hip_to_foot / dist_hip_to_hip
    prepared_instructions = {0: "don't lean your upper body over towards the camera",
                             1: "stand on the center of the sole, instead of the sides, of your feet",
                             2: "try to lower your hip below the top of your knees",
                             3: "keep your knees pointing to the front direction and your legs parallel to "
                                "each other",
                             4: "are you feeling pain? if so, stop the exercise immediately!"
                             }

    if not angle_in_range(left_knee_angle_from_front, 25, 45) or not angle_in_range(right_knee_angle_from_front, 25,
                                                                                    45):
        yield prepared_instructions[3]
    if dist_hip_to_foot > dist_knee_to_foot:
        yield prepared_instructions[2]
