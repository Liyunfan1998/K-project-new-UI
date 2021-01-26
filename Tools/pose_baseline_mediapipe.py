from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Tools.procrustes as procrustes
import Tools.viz as viz
import Tools.cameras as cameras
import Tools.data_utils as data_utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tensorflow.compat.v1 as tf

tf.disable_eager_execution()

import os
import time
import imageio
from Tools.linear_model_openpose import LinearModel


class Lifter:
    def __init__(self, base=os.getcwd() + '/Tools/'):
        train_dir = os.path.join('')
        summaries_dir = os.path.join(train_dir, "log")
        # base = os.getcwd() + '/Tools/'
        mean_std_3d = np.load(base + 'h36m-3d-mean-std.npz')
        mean_std = np.load(base + 'mediapipe-mean-std.npz')
        self.data_mean_3d, self.data_std_3d, self.dim_to_ignore_3d = mean_std_3d['data_mean_3d'], mean_std_3d[
            'data_std_3d'], \
                                                                     mean_std_3d['dim_to_ignore_3d']
        device_count = {"GPU": 1}
        tf.reset_default_graph()
        self.sess = tf.Session(config=tf.ConfigProto(device_count=device_count, allow_soft_placement=True))
        self.model = LinearModel(1024, 2, True, True, True, 64, 0.001, summaries_dir)
        self.sess.run(tf.global_variables_initializer())
        self.model.train_writer.add_graph(self.sess.graph)

        self.model.saver.restore(self.sess, base + 'checkpoint-2402400')
        self.data_mean_2d, self.data_std_2d = mean_std['data_mean'], mean_std['data_std']

        self._max = 0
        self._min = 10000

        self.all_poses_3d = []
        self.frame = -1
        self.png_lib = []

    def get_3d_joints(self, mp_out):  # mp_out should be of shape (132)
        xyzv = mp_out
        self.frame += 1
        enc_in = np.divide((xyzv - self.data_mean_2d), self.data_mean_2d).reshape(1, 132)
        dec_out = np.zeros((1, 36))
        _, _, poses3d = self.model.step(self.sess, enc_in, dec_out, 1, isTraining=False)
        poses3d = data_utils.unNormalizeData(poses3d, self.data_mean_3d, self.data_std_3d, self.dim_to_ignore_3d)

        # spin is the middle point of #11 and #12
        # spine_x, spine_y = np.mean([xyzv[44], xyzv[48]]), np.mean([xyzv[45], xyzv[49]])
        # enc_in = data_utils.unNormalizeData(enc_in, self.data_mean_2d, self.data_std_2d, [])
        #
        # self.all_poses_3d.append(poses3d)
        # enc_in, poses3d = map(np.vstack, [enc_in, self.all_poses_3d])
        #
        # for i in range(poses3d.shape[0]):
        #     for j in range(32):
        #         tmp = poses3d[i][j * 3 + 2]
        #         poses3d[i][j * 3 + 2] = poses3d[i][j * 3 + 1]
        #         poses3d[i][j * 3 + 1] = tmp
        #         if poses3d[i][j * 3 + 2] > self._max:
        #             self._max = poses3d[i][j * 3 + 2]
        #         if poses3d[i][j * 3 + 2] < self._min:
        #             self._min = poses3d[i][j * 3 + 2]
        #
        # for i in range(poses3d.shape[0]):
        #     for j in range(32):
        #         poses3d[i][j * 3 + 2] = (self._max - poses3d[i][j * 3 + 2] + self._min)
        #         poses3d[i][j * 3] += (spine_x - 630)
        #         poses3d[i][j * 3 + 2] += (500 - spine_y)
        return poses3d

        # gs1 = gridspec.GridSpec(1, 1)
        # gs1.update(wspace=-0.00, hspace=0.05)
        # plt.axis('off')
        # subplot_idx, exidx = 1, 1
        #     ax = plt.subplot(gs1[subplot_idx - 1], projection='3d')
        #     ax.view_init(18, -70)
        #     viz.show3Dpose(poses3d[-1], ax, lcolor="#9b59b6", rcolor="#2ecc71")
        #
        #     pngName = 'out_png/pose_frame_{0}.png'.format(str(frame).zfill(12))
        #     plt.savefig(pngName)
        #     png_lib.append(imageio.imread(pngName))
        # np.savez('pose3d.npz', pose3d=all_poses_3d)


'''if __name__ == '__main__':
    import mediapipe as mp

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    import cv2

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 10)
    while cap.isOpened():
        ret, image = cap.read()
        image = cv2.flip(image, 1)
        results = pose.process(image)
        xyzv = []
        if results.pose_landmarks is not None:
            for landmark in results.pose_landmarks.landmark:
                xyzv.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            print(len(xyzv))
            lifter = Lifter()
            poses3d = lifter.get_3d_joints(xyzv)
            print(poses3d)

    cap.release()
    pose.release()'''
