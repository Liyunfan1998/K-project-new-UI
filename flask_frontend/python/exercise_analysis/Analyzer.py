import pyttsx3

from Analysis_utils import *


class Analyzer():
    def scoreFMSmovement(self, movementName=None, uvzv=None, depth_points=None):
        if movementName == 'squat':
            scoreSquat(uvzv, depth_points)
        elif movementName == 'hurdle':
            scoreHurdle(uvzv, depth_points)
        elif movementName == 'raiseLeg':
            scoreRaiseLeg(uvzv, depth_points)

    # TODO: add analysis module and embed the tts engine in it
    # https://zhuanlan.zhihu.com/p/37923715
    # https://zhuanlan.zhihu.com/p/38136322

    def to_voice(self, engine=None, string='this is a test'):
        engine = pyttsx3.init()
        engine.say(string)
        engine.runAndWait()
