import tkinter as tk
import threading
import time
import pyrealsense2 as rs
from configs.MediaPipe_DrawConfig import *


def _cal_angle(vec1, vec2):
    cos_ = vec1.dot(vec2) / (np.sqrt(vec1.dot(vec1)) * np.sqrt(vec2.dot(vec2)))
    return 0 if cos_ == np.nan else np.arccos(cos_) * 180 / np.pi


def _get_bone_vec_mp(xyz, start_idx, end_idx, dim):
    return xyz[start_idx, :dim] - xyz[end_idx, :dim]


def get_bone_angle(xyz, connections=None, bone_pairs=None, dim=3):
    res = dict()
    bone_vecs = [_get_bone_vec_mp(xyz, con[0], con[1], dim=dim) for con in connections]
    for key, (bone1_idx, bone2_idx) in bone_pairs.items():
        res[key] = _cal_angle(bone_vecs[bone1_idx], bone_vecs[bone2_idx])
    return res


#################### For Openpose ###########################
def get_bone_angle_OP(xyv, dim=3):
    return get_bone_angle(xyv, conns_op, bone_idx_pairs_op, dim)


def getCameraSpacePointCoords(uvzv, depth_intrin, depthframe):
    # TODO: only get the joint_vecs when visible
    uvzv = uvzv.astype(np.int)
    return [rs.rs2_deproject_pixel_to_point(depth_intrin, [uvzv[i][0], uvzv[i][1]],
                                            depthframe.get_distance(uvzv[i][0], uvzv[i][1])) for i in range(33)]


def show_angle_on_joints(uvzv, depth_points=None, dim=3):
    pos_angle_dict = dict()
    xy = uvzv[:, :2].astype('int')
    if depth_points is not None:  # realsense
        angles = get_bone_angle(depth_points, POSE_CONNECTIONS, bone_idx_pairs_all, dim=dim)
    else:  # webcam
        angles = get_bone_angle(uvzv, POSE_CONNECTIONS, bone_idx_pairs_all, dim=dim)
    for joint_name, joint_idx in draw_text_pos_joint.items():
        pos_angle_dict[joint_name] = xy[joint_idx], angles[joint_name]
    return pos_angle_dict


class App(threading.Thread):
    """
    instance of this class can capture keyboard events in  a non-blocking way
    It is intend to track start and stop signals from the remote controller
    On Start and On Stop is the trigger for saving png images
    this is useful when aligning start-time between realsense and vicon
    and is also useful when the system is used by a patient, in which case the patient use it to indicate pain, shaking and calling-for-help
    """

    def __init__(self, state_dict=None):
        print("### Start listening to press event ###")
        # print('Now we can continue running code while mainloop runs!')
        threading.Thread.__init__(self)
        self.state_dict = state_dict
        self.fo = open("press.txt", "a")
        self.start()

    def onKeyPress(self, event=None):
        stime = str(time.time())
        print('%s\tYou pressed %s\n' % (stime, event.keycode,))
        self.fo.write(stime + '\n')
        self.fo.flush()

    def onPgDnPress(self, event):  # Stop Recording
        self.state_dict['isShowOnFlask'] = False
        print("stop saving pngs")
        self.onKeyPress(event)

    def onPgUpPress(self, event):  # Start Recording
        self.state_dict['isShowOnFlask'] = True
        print("start inferencing")
        self.onKeyPress(event)

    def callback(self):
        self.fo.close()
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        # self.root.withdraw()
        self.root.iconify()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.bind("<Next>", self.onPgDnPress)  # Bind to PageDown
        self.root.bind("<Prior>", self.onPgUpPress)  # Bind to PageUp
        self.root.mainloop()
