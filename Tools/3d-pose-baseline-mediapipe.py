from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
import numpy as np
import torch
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow.compat.v1 as tf
import Tools.procrustes as procrustes

import Tools.viz as viz
import Tools.cameras as cameras
import Tools.data_utils as data_utils
import inspect
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tensorflow.compat.v1 as tf
import os
import time
import imageio
from Tools.linear_model_openpose import LinearModel

train_dir = os.path.join('')
summaries_dir = os.path.join(train_dir, "log")

'''train_dir = os.path.join("experiments", 'All', 'dropout_0.5', 'epochs_{0}'.format(100), 'lr_0.001', 'residual',
                         'depth_2', 'linear_size1024', 'batch_size_64', 'no_procrustes', 'maxnorm''batch_normalization',
                         'use_mediapipe', 'predict_17')
print(train_dir)
summaries_dir = os.path.join(train_dir, "log")
os.system('mkdir -p {}'.format(summaries_dir))

actions = data_utils.define_actions("All")

# Load camera parameters
SUBJECT_IDS = [1, 5, 6, 7, 8, 9, 11]
rcams = cameras.load_cameras("data/Release-v1.2/metadata.xml", SUBJECT_IDS)

train_set_2d, test_set_2d, train_frame_seq, test_frame_seq, data_mean_2d, data_std_2d = data_utils.create_mediapipe_2D_data(
    actions, "mph36m/", rcams)
# data_mean_2d, data_std_2d, dim_to_use_2d, dim_to_ignore_2d = None, None, None, None


# In[98]:


# Load 3d data and load (or create) 2d projections
train_set_3d, test_set_3d, data_mean_3d, data_std_3d, dim_to_ignore_3d, dim_to_use_3d, train_root_positions, test_root_positions = data_utils.read_3d_data(
    actions, "data/h36m/", True, rcams, False)

# In[108]:


train_set_3d = {key: value for key, value in train_set_3d.items() if key in train_frame_seq.keys()}
test_set_3d = {key: value for key, value in test_set_3d.items() if key in test_frame_seq.keys()}
train_set_2d = {key: value for key, value in train_set_2d.items() if key in train_set_3d.keys()}
test_set_2d = {key: value for key, value in test_set_2d.items() if key in test_set_3d.keys()}
train_frame_seq = {key: value for key, value in train_frame_seq.items() if key in train_set_3d.keys()}
test_frame_seq = {key: value for key, value in test_frame_seq.items() if key in test_set_3d.keys()}
len(test_set_2d.keys()), len(test_set_3d.keys()), len(train_set_2d.keys()), len(train_set_3d.keys()), len(
    train_frame_seq.keys()), len(test_frame_seq.keys())

# In[100]:


for key in set(train_set_2d.keys()) & set(train_set_3d.keys()):
    if np.array(train_set_2d[key]).shape[0] != np.array(train_set_3d[key]).shape[0]:
        print(key, np.array(train_set_2d[key]).shape, np.array(train_set_3d[key]).shape)

# In[102]:


dim_to_use_2d, dim_to_ignore_2d = None, None

# In[104]:


def set_2D_used_seq(train_set_3d, test_set_3d, train_set_2d, test_set_2d):
    for key in train_set_2d.keys():
        train_3d_len = len(train_set_3d[key])
        train_set_2d[key] = train_set_2d[key][:train_3d_len]
        train_frame_seq[key] = [i for i in train_frame_seq[key] if i < train_3d_len]
    for key in test_set_2d.keys():
        test_3d_len = len(test_set_3d[key])
        test_set_2d[key] = test_set_2d[key][:test_3d_len]
        test_frame_seq[key] = [i for i in test_frame_seq[key] if i < test_3d_len]


set_2D_used_seq(train_set_3d, test_set_3d, train_set_2d, test_set_2d)


# In[109]:


def set_3D_used_seq(train_set_3d, test_set_3d, train_set_2d, test_set_2d):
    for key in train_set_2d.keys():
        train_set_2d[key] = train_set_2d[key][train_frame_seq[key]]
        train_set_3d[key] = train_set_3d[key][train_frame_seq[key]]
    for key in test_set_2d.keys():
        test_set_2d[key] = test_set_2d[key][test_frame_seq[key]]
        test_set_3d[key] = test_set_3d[key][test_frame_seq[key]]


set_3D_used_seq(train_set_3d, test_set_3d, train_set_2d, test_set_2d)

# In[111]:


for key in set(train_set_2d.keys()) & set(train_set_3d.keys()):
    print(key, np.array(train_set_2d[key]).shape, np.array(train_set_3d[key]).shape)


# In[112]:


def get_action_subset(poses_set, action):
    return {k: v for k, v in poses_set.items() if k[1] == action}


def evaluate_batches(sess, model,
                     data_mean_3d, data_std_3d, dim_to_use_3d, dim_to_ignore_3d,
                     data_mean_2d, data_std_2d, dim_to_use_2d, dim_to_ignore_2d,
                     current_step, encoder_inputs, decoder_outputs, current_epoch=0):
    n_joints = 13
    nbatches = len(encoder_inputs)

    # Loop through test examples
    all_dists, start_time, loss = [], time.time(), 0.
    log_every_n_batches = 100
    for i in range(nbatches):

        if current_epoch > 0 and (i + 1) % log_every_n_batches == 0:
            print("Working on test epoch {0}, batch {1} / {2}".format(current_epoch, i + 1, nbatches))

        enc_in, dec_out = encoder_inputs[i], decoder_outputs[i]
        dp = 1.0  # dropout keep probability is always 1 at test time
        step_loss, loss_summary, poses3d = model.step(sess, enc_in, dec_out, dp, isTraining=False)
        loss += step_loss

        # denormalize
        dec_out = data_utils.unNormalizeData(dec_out, data_mean_3d, data_std_3d, dim_to_ignore_3d)
        poses3d = data_utils.unNormalizeData(poses3d, data_mean_3d, data_std_3d, dim_to_ignore_3d)

        # Keep only the relevant dimensions
        dtu3d = np.hstack((np.arange(3), dim_to_use_3d)) if not False else dim_to_use_3d

        dec_out = dec_out[:, dtu3d]
        poses3d = poses3d[:, dtu3d]

        if False:
            # Apply per-frame procrustes alignment if asked to do so
            for j in range(64):
                gt = np.reshape(dec_out[j, :], [-1, 3])
                out = np.reshape(poses3d[j, :], [-1, 3])
                _, Z, T, b, c = procrustes.compute_similarity_transform(gt, out, compute_optimal_scale=True)
                out = (b * out.dot(T)) + c
                poses3d[j, :] = np.reshape(out, [-1, 13 * 3])

        # Compute Euclidean distance error per joint
        sqerr = (poses3d - dec_out) ** 2  # Squared error between prediction and expected output
        dists = np.zeros((sqerr.shape[0], n_joints))  # Array with L2 error per joint in mm
        dist_idx = 0
        for k in np.arange(0, n_joints * 3, 3):
            # Sum across X,Y, and Z dimenstions to obtain L2 distance
            dists[:, dist_idx] = np.sqrt(np.sum(sqerr[:, k:k + 3], axis=1))
            dist_idx = dist_idx + 1

        all_dists.append(dists)
    step_time = (time.time() - start_time) / nbatches
    loss = loss / nbatches

    all_dists = np.vstack(all_dists)

    # Error per joint and total for all passed batches
    joint_err = np.mean(all_dists, axis=0)
    total_err = np.mean(all_dists)

    return total_err, joint_err, step_time, loss


# In[113]:


device_count = {"GPU": 1}
tf.reset_default_graph()
sess = tf.Session(config=tf.ConfigProto(
    device_count=device_count,
    allow_soft_placement=True))

from linear_model_openpose import LinearModel

tf.reset_default_graph()
with sess:
    model = LinearModel(1024, 2, True, True, True, 64, 0.001, summaries_dir)
    sess.run(tf.global_variables_initializer())
    model.train_writer.add_graph(sess.graph)

    # === This is the training loop ===
    step_time, loss, val_loss = 0.0, 0.0, 0.0
    load = 0
    current_step = 0 if load <= 0 else load + 1
    previous_losses = []

    step_time, loss = 0, 0
    current_epoch = 0
    log_every_n_batches = 10000
    for _ in xrange(100):
        current_epoch = current_epoch + 1

        # === Load training batches for one epoch ===
        encoder_inputs, decoder_outputs = model.get_all_batches(train_set_2d, train_set_3d, True, training=True)
        nbatches = len(encoder_inputs)
        print("There are {0} train batches".format(nbatches))
        start_time, loss = time.time(), 0.

        for i in range(nbatches):
            if (i + 1) % log_every_n_batches == 0:
                print("Working on epoch {0}, batch {1} / {2}... ".format(current_epoch, i + 1, nbatches), end="")

            enc_in, dec_out = encoder_inputs[i], decoder_outputs[i]
            step_loss, loss_summary, lr_summary, _ = model.step(sess, enc_in, dec_out, .5, isTraining=True)

            if (i + 1) % log_every_n_batches == 0:
                # Log and print progress every log_every_n_batches batches
                model.train_writer.add_summary(loss_summary, current_step)
                model.train_writer.add_summary(lr_summary, current_step)
                step_time = (time.time() - start_time)
                start_time = time.time()
                print("done in {0:.2f} ms".format(1000 * step_time))

            loss += step_loss
            current_step += 1
            # === end looping through training batches ===

        loss = loss / nbatches
        print("=============================\n"
              "Global step:         %d\n"
              "Learning rate:       %.2e\n"
              "Train loss avg:      %.4f\n"
              "=============================" % (model.global_step.eval(),
                                                 model.learning_rate.eval(), loss))
        # === Testing after this epoch ===
        isTraining = False
        print("{0:=^12} {1:=^6}".format("Action", "mm"))  # line of 30 equal signs

        cum_err = 0
        for action in actions:
            print("{0:<12} ".format(action), end="")
            action_test_set_2d = get_action_subset(test_set_2d, action)
            action_test_set_3d = get_action_subset(test_set_3d, action)
            encoder_inputs, decoder_outputs = model.get_all_batches(action_test_set_2d, action_test_set_3d,
                                                                    True, training=False)
            act_err, _, step_time, loss = evaluate_batches(sess, model,
                                                           data_mean_3d, data_std_3d, dim_to_use_3d,
                                                           dim_to_ignore_3d,
                                                           data_mean_2d, data_std_2d, dim_to_use_2d,
                                                           dim_to_ignore_2d,
                                                           current_step, encoder_inputs, decoder_outputs)
            cum_err = cum_err + act_err

            print("{0:>6.2f}".format(act_err))

        summaries = sess.run(model.err_mm_summary, {model.err_mm: float(cum_err / float(len(actions)))})
        model.test_writer.add_summary(summaries, current_step)
        print("{0:<12} {1:>6.2f}".format("Average", cum_err / float(len(actions))))
        print("{0:=^19}".format(''))

        # Save the model
        print("Saving the model... ", end="")
        start_time = time.time()
        model.saver.save(sess, os.path.join(train_dir, 'checkpoint'), global_step=current_step)
        print("done in {0:.2f} ms".format(1000 * (time.time() - start_time)))

        # Reset global time and loss
        step_time, loss = 0, 0

        sys.stdout.flush()

order = [15, 12, 25, 26, 27, 17, 18, 19, 1, 2, 3, 6, 7, 8]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def show_anim_curves(anim_dict, _plt):
    val = np.array(list(anim_dict.values()))
    for o in range(0, 36, 2):
        x = val[:, o]
        y = val[:, o + 1]
        _plt.plot(x, 'r--', linewidth=0.2)
        _plt.plot(y, 'g', linewidth=0.2)
    return _plt


# In[42]:


import pandas as pd

smoothed = pd.read_csv(
    '/home/lyunfan/NYU_summer_intern/3d-pose-baseline-with-lifting/src/mp_nyu/NYU_summer_intern_data201909050914301.csv').to_numpy()[
           :, 1:]
smoothed.shape

# In[49]:
'''

ckpt = tf.train.get_checkpoint_state('.', latest_filename="checkpoint")

mean_std_3d = np.load('h36m-3d-mean-std.npz')
data_mean_3d, data_std_3d, dim_to_ignore_3d = mean_std_3d['data_mean_3d'], mean_std_3d['data_std_3d'], mean_std_3d[
    'dim_to_ignore_3d']

device_count = {"GPU": 1}

tf.reset_default_graph()
png_lib = []
with tf.Session(config=tf.ConfigProto(device_count=device_count, allow_soft_placement=True)) as sess:
    model = LinearModel(1024, 2, True, True, True, 64, 0.001, summaries_dir)
    sess.run(tf.global_variables_initializer())
    model.train_writer.add_graph(sess.graph)
    batch_size = 64
    ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
    print("Loading model {0}".format(ckpt_name))
    model.saver.restore(sess, ckpt.model_checkpoint_path)
    mean_std = np.load('mediapipe-mean-std.npz')
    mu, stddev = data_mean_2d, data_std_2d = mean_std['data_mean'], mean_std['data_std']
    frame = -1
    all_poses_3d = []
    for xyzv in smoothed:
        frame += 1
        #         if frame%10!=0: continue
        # spin is the middle point of #11 and #12
        spine_x, spine_y = np.mean([xyzv[44], xyzv[48]]), np.mean([xyzv[45], xyzv[49]])
        #         print(spine_x*1000,spine_y*1000) #464 576
        enc_in = xyzv
        enc_in = np.divide((enc_in - mu), stddev).reshape(1, 132)
        dec_out = np.zeros((1, 36))
        _, _, poses3d = model.step(sess, enc_in, dec_out, 1, isTraining=False)
        enc_in = data_utils.unNormalizeData(enc_in, data_mean_2d, data_std_2d, [])
        poses3d = data_utils.unNormalizeData(poses3d, data_mean_3d, data_std_3d, dim_to_ignore_3d)
        gs1 = gridspec.GridSpec(1, 1)
        gs1.update(wspace=-0.00, hspace=0.05)
        plt.axis('off')
        all_poses_3d.append(poses3d)
        enc_in, poses3d = map(np.vstack, [enc_in, all_poses_3d])
        subplot_idx, exidx = 1, 1

        _max = 0
        _min = 10000

        for i in range(poses3d.shape[0]):
            for j in range(32):
                tmp = poses3d[i][j * 3 + 2]
                poses3d[i][j * 3 + 2] = poses3d[i][j * 3 + 1]
                poses3d[i][j * 3 + 1] = tmp
                if poses3d[i][j * 3 + 2] > _max:
                    _max = poses3d[i][j * 3 + 2]
                if poses3d[i][j * 3 + 2] < _min:
                    _min = poses3d[i][j * 3 + 2]

        for i in range(poses3d.shape[0]):
            for j in range(32):
                poses3d[i][j * 3 + 2] = (_max - poses3d[i][j * 3 + 2] + _min)
                poses3d[i][j * 3] += (spine_x - 630)
                poses3d[i][j * 3 + 2] += (500 - spine_y)

        ax = plt.subplot(gs1[subplot_idx - 1], projection='3d')
        ax.view_init(18, -70)
        viz.show3Dpose(poses3d[-1], ax, lcolor="#9b59b6", rcolor="#2ecc71")

        pngName = 'out_png/pose_frame_{0}.png'.format(str(frame).zfill(12))
        plt.savefig(pngName)
        png_lib.append(imageio.imread(pngName))
    np.savez('pose3d.npz', pose3d=all_poses_3d)

# imageio.mimsave('gif_output/animation.gif', png_lib, fps=24)
#
# ax = plt.subplot(gs1[subplot_idx - 1], projection='3d')
# ax.view_init(18, -70)
# viz.show3Dpose(poses3d[2], ax, lcolor="#9b59b6", rcolor="#2ecc71")
