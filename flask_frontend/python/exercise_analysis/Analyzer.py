import pyttsx3

from Analysis_utils import *


class Analyzer:
    score = None
    subItemDict = None
    movementName = None

    def __init__(self, movementName=None):
        self.movementName = movementName

    def coreFMSmovement(self, uvzv=None, depth_points=None):
        if self.movementName == 'squat':
            self.score, self.subItemDict = scoreSquat(uvzv, depth_points)
        elif self.movementName == 'hurdle':
            self.score, self.subItemDict = scoreHurdle(uvzv, depth_points)
        elif self.movementName == 'raiseLeg':
            self.score, self.subItemDict = scoreRaiseLeg(uvzv, depth_points)

    # TODO: add analysis module and embed the tts engine in it
    # https://zhuanlan.zhihu.com/p/37923715
    # https://zhuanlan.zhihu.com/p/38136322

    def to_voice(self, engine=None, string='this is a test'):
        engine = pyttsx3.init()
        engine.say(string)
        engine.runAndWait()
