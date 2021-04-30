from .Analysis_utils import *
from enum import Enum, unique


@unique
class ScoringStage(Enum):
    START = 0
    END = 1


def pushUp(both_legs_straight, angle_leg_spine, scoringStage=ScoringStage.START):
    '''
    analyze the squat motion and give instructions to patients
    :param both_legs_straight:
    :param angle_leg_spine:
    :return:
    :return: list of strings, which are instructions for the patient, to be turned to voice messages by pyttsx3 engine
    '''

    prepared_instructions = {0: "please keep your legs straight",
                             1: "please lift you hip higher",
                             2: "are you feeling pain? if so, stop the exercise immediately!"
                             }
    # ALWAYS
    if not both_legs_straight:
        yield prepared_instructions[0]

    # START
    # 胸部和腹部需要同时离开地面

    # END
    if angle_in_range(angle_leg_spine, 0, 180):
        # TODO : need fix
        yield prepared_instructions[1]
