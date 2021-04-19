from .Analysis_utils import *


def hurdle(angle_knee_to_ankle_to_foot_index, dist_foot_to_foot, dist_knee_to_foot, angle_hip_level_shoulder_level,
           is_knee_valgus, using_support_pad=False):
    '''
    analyze the squat motion and give instructions to patients
    :param angle_knee_to_ankle_to_foot_index:
    :param dist_foot_to_foot:
    :param dist_knee_to_foot:
    :param angle_hip_level_shoulder_level:
    :param is_knee_valgus:
    :param using_support_pad:
    :return: list of strings, which are instructions for the patient, to be turned to voice messages by pyttsx3 engine
    '''

    prepared_instructions = {0: "please keep your body straight up",
                             1: "please keep your foot level to the ground and point it to the front direction",
                             2: "please raise your foot above your other knee",
                             3: "please point your knee to the front direction",
                             4: "are you feeling pain? if so, stop the exercise immediately!"
                             }

    is_body_straight = angle_hip_level_shoulder_level
    is_hurdle_foot_above_knee = dist_foot_to_foot > dist_knee_to_foot

    if not is_body_straight:
        yield prepared_instructions[0]
    if not angle_in_range(angle_knee_to_ankle_to_foot_index, 30, 90):
        yield prepared_instructions[1]
    if not not is_hurdle_foot_above_knee:
        yield prepared_instructions[2]
    if is_knee_valgus:
        yield prepared_instructions[3]
