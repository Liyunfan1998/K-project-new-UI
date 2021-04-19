import numpy as np
from .vid2pose_config import *


def get_bone_angle(xyzv, bone_idx_pairs, dim=3):
    def _get_bone_vec(xyzv, start_idx, end_idx):
        return np.array(xyzv[end_idx * 4:end_idx * 4 + dim]) - np.array(xyzv[start_idx * 4:start_idx * 4 + dim])

    def _get_all_bone_vecs(xyzv):
        all_bone_vecs = []
        for connection in POSE_CONNECTIONS:
            all_bone_vecs.append(_get_bone_vec(xyzv, start_idx=connection[0], end_idx=connection[1], dim=3))
        return all_bone_vecs

    def _cal_angle(x, y):
        cos_ = x.dot(y) / (np.sqrt(x.dot(x)) * np.sqrt(y.dot(y)))
        return np.arccos(cos_) * 180 / np.pi

    res = dict()
    bones = [_get_bone_vec(xyzv, con[0], con[1]) for con in conns]

    for key, (bone1_idx, bone2_idx) in bone_idx_pairs.items():
        res[key] = _cal_angle(bones[bone1_idx], bones[bone2_idx])
    return res

