
conns_op = [[0, 1],  # 0 neck
            [1, 2],  # 1 left shoulder-neck
            [2, 3],  # 2 left big arm
            [3, 4],  # 3 left small arm
            [1, 5],  # 4 right shoulder-neck
            [5, 6],  # 5 right big arm
            [6, 7],  # 6 right small arm
            [1, 8],  # 7 spine
            [8, 9],  # 8 left spine-thigh
            [9, 10],  # 9 left thigh
            [10, 11],  # 10 left small leg
            [8, 12],  # 11 right spine-thigh
            [12, 13],  # 12 right thigh
            [13, 14],  # 13 right small leg
            [2, 5],  # 14 shoulder-horiz
            [9, 12],  # 15 hip-horiz
            ]
# up2down, left2right
bone_idx_pairs_op = {'left-big-small-arm': (1, 2), 'right-big-small-arm': (5, 6),
                     'left-spin-big-arm': (7, 2), 'right-spin-big-arm': (7, 5),
                     'left-spin-thigh': (7, 9), 'right-spin-thigh': (7, 12),
                     'left-spin-small-leg': (7, 10), 'right-spin-small-leg': (7, 13),
                     'left-upper-lower-leg': (9, 10), 'right-upper-lower-leg': (12, 13),
                     'shoulder-horiz-hip-horiz': (14, 15)
                     }
