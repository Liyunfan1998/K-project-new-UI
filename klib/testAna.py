from klib.analysis import Analysis
from klib.initial_param.kparam import *
from klib.human_model import Human_model
import numpy as np

# Predefined param

ana = Analysis()
exeno = 4
kp = Kparam(exeno, "test_user")
body = np.random.rand(26, 3)  # np.ndarray((26, 3), dtype=np.int)
h_mod = Human_model()
modJary = h_mod.human_mod_pts(body, False)  # modJary is 11*3 array
reconJ = modJary.flatten().reshape(-1, 33)  # change shape to 1*33 array


def MapCameraPointToDepthSpace():
    pass


def body_joints_to_depth_space(joints, JointType_Count=25):
    joint_points = np.ndarray((JointType_Count), dtype=np.object)
    for j in range(0, JointType_Count):
        joint_points[j] = MapCameraPointToDepthSpace(joints[j].Position)
    return joint_points


# djps = body_joints_to_depth_space(joints)  # joint points in depth domain

"""
# joint order in kinect
        self.JointType_SpineBase     = 0
        self.JointType_SpineMid      = 1
        self.JointType_Neck          = 2
        self.JointType_Head          = 3
        self.JointType_ShoulderLeft  = 4
        self.JointType_ElbowLeft     = 5
        self.JointType_WristLeft     = 6
        self.JointType_HandLeft      = 7
        self.JointType_ShoulderRight = 8
        self.JointType_ElbowRight    = 9
        self.JointType_WristRight    = 10
        self.JointType_HandRight     = 11
        self.JointType_HipLeft       = 12
        self.JointType_KneeLeft      = 13
        self.JointType_AnkleLeft     = 14
        self.JointType_FootLeft      = 15
        self.JointType_HipRight      = 16
        self.JointType_KneeRight     = 17
        self.JointType_AnkleRight    = 18
        self.JointType_FootRight     = 19
        self.JointType_SpineShoulder = 20
        self.JointType_HandTipLeft   = 21
        self.JointType_ThumbLeft     = 22
        self.JointType_HandTipRight  = 23
        self.JointType_ThumbRight    = 24
        self.JointType_Count         = 25
        """

"""
Body:   11 joints
        self.JointType_SpineBase     = 0
        self.JointType_SpineMid      = 1
        self.JointType_Neck          = 2
        self.JointType_Head          = 3
        self.JointType_ShoulderLeft  = 4
        self.JointType_ElbowLeft     = 5
        self.JointType_WristLeft     = 6
        self.JointType_ShoulderRight = 8
        self.JointType_ElbowRight    = 9
        self.JointType_WristRight    = 10
        self.JointType_SpineShoulder = 20
"""

# run(self, exeno, reconJ, surface=None, evalinst=None, kp=None, body=None, dmap=[], djps=[])

# ana.run(exeno=exeno, reconJ=reconJ[0], surface=None, evalinst=None, kp=kp, body=None, dmap=None, djps=None)
ana.testExeNo4(exeno=exeno, reconJ=reconJ[0], surface=None, evalinst=None, kp=kp, body=None, dmap=None, djps=None)
