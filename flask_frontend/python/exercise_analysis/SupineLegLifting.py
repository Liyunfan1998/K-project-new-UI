from .Analysis_utils import *


def supineLegLifing(both_legs_straight, angle_left_leg_right_leg):
    '''
    analyze the squat motion and give instructions to patients
    :param both_legs_straight:
    :param angle_left_leg_right_leg:
    :return:
    :return: list of strings, which are instructions for the patient, to be turned to voice messages by pyttsx3 engine
    '''

    prepared_instructions = {0: "please keep your legs straight",
                             1: "please lift you leg higher",
                             2: "are you feeling pain? if so, stop the exercise immediately!"
                             }

    if not both_legs_straight:
        yield prepared_instructions[0]
    if angle_in_range(angle_left_leg_right_leg,0,30):
        yield