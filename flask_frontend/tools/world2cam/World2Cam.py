import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description="world to cam")
parser.add_argument("-p", default="F:/robolab/rehabilitation/vicon")
parser.add_argument("-c", default="lirui03.mp4.csv")
parser.add_argument("-w", default="lirui Cal 03.csv")
args = parser.parse_args()

outputPath = args.p + '/' + 'world2cam.csv'
camCsvPath = args.p + '/' + args.c
worldCsvPath = args.p + '/' + args.w

width = 640
height = 480
colorIntri = np.array([[608.034, 0, 320.775], [0, 606.833, 235.443], [0, 0, 1]], dtype=np.float64)
distCoeffs = np.zeros((4, 1), dtype=np.float64)
pointsCam = []
pointsWorld = []
sampleTime = []
pose_mat = np.zeros((3, 4), dtype=np.float64)

# 趴下姿势，所以右侧是看得到左侧看不到
# 选择右侧shoulder，hip，knee，ankle四个关节
# https://google.github.io/mediapipe/solutions/pose#pose_landmarks
mediaPipeIdx = [12, 24, 26, 28]
# mediapipe的csv文件中，稳定读数从该开始
mediaPipeBegin = 100

# vicon数据中对应关节的excel列号
viconIdx = ["42", "15", "84+87", "114+117"]


def calTrans():
    global colorIntri, distCoeffs, pointsCam, pointsWorld, pose_mat
    npCam = np.array(pointsCam, dtype=np.float64)
    npWorld = np.array(pointsWorld, dtype=np.float64)
    res, rvec, tvec, inliers = cv2.solvePnPRansac(npWorld, npCam, colorIntri, distCoeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    rotM = cv2.Rodrigues(rvec)[0]
    pose_mat = cv2.hconcat((rotM, tvec))  # 3x4


# 功能:计算外参矩阵，并根据算出的外参矩阵，将世界三维坐标反求到相机图像坐标系，并与pointsCam对比
def solveMatrix():
    global colorIntri, distCoeffs, pointsCam, pointsWorld, pose_mat
    calTrans()
    pwT = np.array(pointsWorld, dtype=np.float64).transpose()
    b = np.ones((1, pwT.shape[1]), dtype=np.float64)
    # pwT是vicon世界坐标系下的关节点坐标
    pwT = np.concatenate((pwT, b), axis=0)
    # pcT是将vicon采集到的真值点坐标，从vicon世界坐标系变换到了相机坐标系下
    pcT = np.matmul(pose_mat, pwT)
    # uvT是将vicon采集到的真值点坐标，从相机坐标系变换到了图像坐标系下
    uvT = np.matmul(colorIntri, pcT)
    for i in range(uvT.shape[1]):
        d = uvT[2][i]
        uvT[0][i] = round(uvT[0][i] / d)
        uvT[1][i] = round(uvT[1][i] / d)
        uvT[2][i] = 1
    print("extrin")
    print(pose_mat)
    print("world2cam")
    print(uvT[0:2])
    print("cam")
    npCam = np.array(pointsCam, dtype=np.float64).transpose()
    print(npCam)


# 功能:读取mediapipe输出的结果文件，将用于匹配的关节点的图像坐标放入pointsCam
def readMP():
    global camCsvPath, mediaPipeBegin, mediaPipeIdx, pointsCam, width, height, sampleTime
    with open(camCsvPath, 'r', encoding='utf-8') as cf:
        numFrames = 0
        for count, line in enumerate(cf.readlines()):
            # 采集帧号和文件行号对齐，采集帧号从0开始
            count -= 1
            if (count >= mediaPipeBegin and count % 15 == 0 and numFrames <= 3):
                numFrames += 1
                lineArr = line.split(',')
                for idx in mediaPipeIdx:
                    # xy坐标放入list当中
                    tmp = [int(float(lineArr[idx * 4 + 1]) * width), int(float(lineArr[idx * 4 + 2]) * height)]
                    pointsCam.append(tmp)
                sampleTime.append(count / 30)
    cf.close()
    # print(pointsCam)
    # print(sampleTime)


# 功能:读取vicon输出的结果文件，将用于匹配的关节点的三维世界坐标放入pointsWorld
def readVC():
    global pointsWorld, worldCsvPath, sampleTime, viconId
    t = 0
    with open(worldCsvPath, 'r', encoding='utf-8') as wf:
        for count, line in enumerate(wf.readlines()):
            # 采集帧号和文件行号对齐，采集帧号从0开始
            count -= 5
            # 在vicon数据中，取出时间相同的帧
            if (t < len(sampleTime) and count * 0.01 == sampleTime[t]):
                t += 1
                lineArr = line.split(',')
                # 每个关节的计算
                for str in viconIdx:
                    strArr = str.split('+')
                    x = 0
                    y = 0
                    z = 0
                    # 一个关节可能是多个标记点取平均
                    for i in range(len(strArr)):
                        x += float(lineArr[int(strArr[i]) - 1]) / len(strArr)
                        y += float(lineArr[int(strArr[i])]) / len(strArr)
                        z += float(lineArr[int(strArr[i]) + 1]) / len(strArr)
                    pointsWorld.append([x, y, z])
    wf.close()
    # print(pointsWorld)


readMP()
readVC()
solveMatrix()
