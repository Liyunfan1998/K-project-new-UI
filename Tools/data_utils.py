import copy
import numpy as np
import Tools.cameras as cameras

# Human3.6m IDs for training and testing
TRAIN_SUBJECTS = [1, 5, 6, 7, 8]
TEST_SUBJECTS = [9, 11]

# Joints in H3.6M -- data has 32 joints, but only 17 that move; these are the indices.
H36M_NAMES = [''] * 32
H36M_NAMES[0] = 'Hip'
H36M_NAMES[1] = 'RHip'
# H36M_NAMES[2] = 'RKnee'
H36M_NAMES[6] = 'LHip'
H36M_NAMES[7] = 'LKnee'
H36M_NAMES[8] = 'LFoot'
H36M_NAMES[12] = 'Spine'
H36M_NAMES[13] = 'Thorax'
H36M_NAMES[14] = 'Neck/Nose'
H36M_NAMES[15] = 'Head'
H36M_NAMES[17] = 'LShoulder'
H36M_NAMES[18] = 'LElbow'
H36M_NAMES[19] = 'LWrist'
H36M_NAMES[25] = 'RShoulder'
H36M_NAMES[26] = 'RElbow'
H36M_NAMES[27] = 'RWrist'

# Stacked Hourglass produces 16 joints. These are the names.
SH_NAMES = [''] * 16
SH_NAMES[0] = 'RFoot'
SH_NAMES[1] = 'RKnee'
SH_NAMES[2] = 'RHip'
SH_NAMES[3] = 'LHip'
SH_NAMES[4] = 'LKnee'
SH_NAMES[5] = 'LFoot'
SH_NAMES[6] = 'Hip'
SH_NAMES[7] = 'Spine'
SH_NAMES[8] = 'Thorax'
SH_NAMES[9] = 'Head'
SH_NAMES[10] = 'RWrist'
SH_NAMES[11] = 'RElbow'
SH_NAMES[12] = 'RShoulder'
SH_NAMES[13] = 'LShoulder'
SH_NAMES[14] = 'LElbow'
SH_NAMES[15] = 'LWrist'

# MideaPipe produces 33 joints. These are the names.
MP_NAMES = [''] * 33
MP_NAMES[0] = 'Nose'
MP_NAMES[1] = 'Left eye inner'
MP_NAMES[2] = 'Left eye'
MP_NAMES[3] = 'Left eye outer'
MP_NAMES[4] = 'Right eye inner'
MP_NAMES[5] = 'Right eye'
MP_NAMES[6] = 'Right eye outer'
MP_NAMES[7] = 'Left ear'
MP_NAMES[8] = 'Right ear'
MP_NAMES[9] = 'Mouth left'
MP_NAMES[10] = 'Mouth right'
MP_NAMES[11] = 'Left shoulder'
MP_NAMES[12] = 'Right shoulder'
MP_NAMES[13] = 'Left elbow'
MP_NAMES[14] = 'Right elbow'
MP_NAMES[15] = 'Left wrist'
MP_NAMES[16] = 'Right wrist'
MP_NAMES[17] = 'Left pinky #1 knuckle'
MP_NAMES[18] = 'Right pinky #1 knuckle'
MP_NAMES[19] = 'Left index #1 knuckle'
MP_NAMES[20] = 'Right index #1 knuckle'
MP_NAMES[21] = 'Left thumb #2 knuckle'
MP_NAMES[22] = 'Right thumb #2 knuckle'
MP_NAMES[23] = 'Left hip'
MP_NAMES[24] = 'Right hip'
MP_NAMES[25] = 'Left knee'
MP_NAMES[26] = 'Right knee'
MP_NAMES[27] = 'Left ankle'
MP_NAMES[28] = 'Right ankle'
MP_NAMES[29] = 'Left heel'
MP_NAMES[30] = 'Right heel'
MP_NAMES[31] = 'Left foot index'
MP_NAMES[32] = 'Right foot index'

not_use_joints = ['', 'LKnee', 'LFoot', 'RKnee', 'RFoot']


def normalization_stats(complete_data, dim, predict_14=False):
    """Computes normalization statistics: mean and stdev, dimensions used and ignored

    Args
      complete_data: nxd np array with poses
      dim. integer={2,3} dimensionality of the data
      predict_14. boolean. Whether to use only 14 joints
    Returns
      data_mean: np vector with the mean of the data
      data_std: np vector with the standard deviation of the data
      dimensions_to_ignore: list of dimensions not used in the model
      dimensions_to_use: list of dimensions used in the model
    """
    if not dim in [2, 3]:
        raise ValueError('dim must be 2 or 3')

    data_mean = np.mean(complete_data, axis=0)
    data_std = np.std(complete_data, axis=0)

    # Encodes which 17 (or 14) 2d-3d pairs we are predicting
    dimensions_to_ignore = []

    if dim == 2:
        # dimensions_to_use = np.where(np.array([x != '' and x != 'Neck/Nose' for x in H36M_NAMES]))[0]
        dimensions_to_use = np.where(np.array([x not in not_use_joints and x != 'Neck/Nose' for x in H36M_NAMES]))[0]
        dimensions_to_use = np.sort(np.hstack((dimensions_to_use * 2, dimensions_to_use * 2 + 1)))
        dimensions_to_ignore = np.delete(np.arange(len(H36M_NAMES) * 2), dimensions_to_use)
    else:  # dim == 3
        # dimensions_to_use = np.where(np.array([x != '' for x in H36M_NAMES]))[0]
        dimensions_to_use = np.where(np.array([x not in not_use_joints for x in H36M_NAMES]))[0]
        dimensions_to_use = np.delete(dimensions_to_use, [0, 7, 9] if predict_14 else 0)

        dimensions_to_use = np.sort(np.hstack((dimensions_to_use * 3,
                                               dimensions_to_use * 3 + 1,
                                               dimensions_to_use * 3 + 2)))
        dimensions_to_ignore = np.delete(np.arange(len(H36M_NAMES) * 3), dimensions_to_use)

    return data_mean, data_std, dimensions_to_ignore, dimensions_to_use


def transform_world_to_camera(poses_set, cams, ncams=4):
    """Project 3d poses from world coordinate to camera coordinate system

    Args
      poses_set: dictionary with 3d poses
      cams: dictionary with cameras
      ncams: number of cameras per subject
    Return:
      t3d_camera: dictionary with 3d poses in camera coordinate
    """
    t3d_camera = {}
    for t3dk in sorted(poses_set.keys()):

        subj, action, seqname = t3dk
        t3d_world = poses_set[t3dk]

        for c in range(ncams):
            R, T, _, _, _, _, name = cams[(subj, c + 1)]
            camera_coord = cameras.world_to_camera_frame(np.reshape(t3d_world, [-1, 3]), R, T)
            camera_coord = np.reshape(camera_coord, [-1, len(H36M_NAMES) * 3])

            sname = seqname[:-3] + name + ".h5"  # e.g.: Waiting 1.58860488.h5
            t3d_camera[(subj, action, sname)] = camera_coord

    return t3d_camera


def normalize_data(data, data_mean, data_std, dim_to_use):
    """Normalizes a dictionary of poses

    Args
      data: dictionary where values are
      data_mean: np vector with the mean of the data
      data_std: np vector with the standard deviation of the data
      dim_to_use: list of dimensions to keep in the data
    Returns
      data_out: dictionary with same keys as data, but values have been normalized
    """
    data_out = {}

    for key in data.keys():
        data[key] = data[key][:, dim_to_use]
        mu = data_mean[dim_to_use]
        stddev = data_std[dim_to_use]
        data_out[key] = np.divide((data[key] - mu), stddev)

    return data_out


def unNormalizeData(normalized_data, data_mean, data_std, dimensions_to_ignore):
    """Un-normalizes a matrix whose mean has been substracted and that has been divided by
    standard deviation. Some dimensions might also be missing

    Args
      normalized_data: nxd matrix to unnormalize
      data_mean: np vector with the mean of the data
      data_std: np vector with the standard deviation of the data
      dimensions_to_ignore: list of dimensions that were removed from the original data
    Returns
      orig_data: the input normalized_data, but unnormalized
    """
    T = normalized_data.shape[0]  # Batch size
    D = data_mean.shape[0]  # Dimensionality

    orig_data = np.zeros((T, D), dtype=np.float32)
    dimensions_to_use = np.array([dim for dim in range(D)
                                  if dim not in dimensions_to_ignore])

    orig_data[:, dimensions_to_use] = normalized_data

    # Multiply times stdev and add the mean
    stdMat = data_std.reshape((1, D))
    stdMat = np.repeat(stdMat, T, axis=0)
    meanMat = data_mean.reshape((1, D))
    meanMat = np.repeat(meanMat, T, axis=0)
    orig_data = np.multiply(orig_data, stdMat) + meanMat
    return orig_data


def define_actions(action):
    """Given an action string, returns a list of corresponding actions.

    Args
      action: String. either "all" or one of the h36m actions
    Returns
      actions: List of strings. Actions to use.
    Raises
      ValueError: if the action is not a valid action in Human 3.6M
    """
    actions = ["Directions", "Discussion", "Eating", "Greeting",
               "Phoning", "Photo", "Posing", "Purchases",
               "Sitting", "SittingDown", "Smoking", "Waiting",
               "WalkDog", "Walking", "WalkTogether"]

    if action == "All" or action == "all":
        return actions

    if not action in actions:
        raise ValueError("Unrecognized action: %s" % action)

    return [action]


def project_to_cameras(poses_set, cams, ncams=4):
    """
    Project 3d poses using camera parameters

    Args
      poses_set: dictionary with 3d poses
      cams: dictionary with camera parameters
      ncams: number of cameras per subject
    Returns
      t2d: dictionary with 2d poses
    """
    t2d = {}

    for t3dk in sorted(poses_set.keys()):
        subj, a, seqname = t3dk
        t3d = poses_set[t3dk]

        for cam in range(ncams):
            R, T, f, c, k, p, name = cams[(subj, cam + 1)]
            pts2d, _, _, _, _ = cameras.project_point_radial(np.reshape(t3d, [-1, 3]), R, T, f, c, k, p)

            pts2d = np.reshape(pts2d, [-1, len(H36M_NAMES) * 2])
            sname = seqname[:-3] + name + ".h5"  # e.g.: Waiting 1.58860488.h5
            t2d[(subj, a, sname)] = pts2d

    return t2d


def postprocess_3d(poses_set):
    """Center 3d points around root

    Args
      poses_set: dictionary with 3d data
    Returns
      poses_set: dictionary with 3d data centred around root (center hip) joint
      root_positions: dictionary with the original 3d position of each pose
    """
    root_positions = {}
    for k in poses_set.keys():
        # Keep track of the global position
        root_positions[k] = copy.deepcopy(poses_set[k][:, :3])

        # Remove the root from the 3d position
        poses = poses_set[k]
        poses = poses - np.tile(poses[:, :3], [1, len(H36M_NAMES)])
        poses_set[k] = poses

    return poses_set, root_positions
