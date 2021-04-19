import pyttsx3

class Analyzer():
    def analyze_pose(self, pose=None):
        self.pose = pose
        # TODO

    # TODO: add analysis module and embed the tts engine in it
    # https://zhuanlan.zhihu.com/p/37923715
    # https://zhuanlan.zhihu.com/p/38136322

    def to_voice(self, engine=None, string='this is a test'):
        engine = pyttsx3.init()
        engine.say(string)
        engine.runAndWait()
