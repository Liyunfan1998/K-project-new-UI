import pyrealsense2 as rs
import numpy as np
import cv2
import time
import os
import h5py
import multiprocessing as mp
from datetime import datetime
import tkinter as tk
import threading

# import pyttsx3


VideoCapture = 0
using_realsense = True


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
        self.state_dict['isSavePNG'] = False
        print("stop saving pngs")
        self.onKeyPress(event)

    def onPgUpPress(self, event):  # Start Recording
        self.state_dict['isSavePNG'] = True
        print("start saving pngs")
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


def get_image_rgb(color_img_q=None, state_dict=None, show=False):
    save_path = "./collect_" + datetime.now().strftime("%m%d%Y_%H_%M_%S") + "/"
    os.mkdir(save_path)
    processes = [
        mp.Process(target=save_png, args=(save_path, color_img_q, state_dict)),
    ]

    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    cap = cv2.VideoCapture(VideoCapture)
    while True:
        success, color_image = cap.read()
        tname = str(time.time()) + '.png'

        color_img_q.put((color_image, color_image, tname))
        # print("color_img_q size: ", color_img_q.qsize())
        color_img_q.get() if color_img_q.qsize() > 1 else None

        # Show images
        if show:
            cv2.imshow('images0', color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


def _start():
    """
    this function runs at the begining of the video capturing process as it warms up the camera by letting go 100 frames (potentially) with fault
    """
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: ", depth_scale)

    align_to = rs.stream.color
    align = rs.align(align_to)
    # 获取图像，realsense刚启动的时候图像会有一些失真，我们保存第100帧图片。
    for i in range(100):
        data = pipeline.wait_for_frames()
        depth = data.get_depth_frame()
        color = data.get_color_frame()

    # 获取内参
    dprofile = depth.get_profile()
    cprofile = color.get_profile()

    cvsprofile = rs.video_stream_profile(cprofile)
    dvsprofile = rs.video_stream_profile(dprofile)

    color_intrin = cvsprofile.get_intrinsics()
    print("color_intrin", color_intrin)
    depth_intrin = dvsprofile.get_intrinsics()
    print("depth_intrin", depth_intrin)

    # 外参
    extrin = dprofile.get_extrinsics_to(cprofile)
    print("extrin", extrin)
    return pipeline, align


def get_image(color_img_q=None, state_dict=None, show=False):
    """
    this function is the main capturing process,
    it runs in a multiprocessing way as the opencv module gets the frames from realsense
    while the spawn of threads saves the frams as color and depth pngs
    """
    pipeline, align = _start()

    save_path = "./collect_" + datetime.now().strftime("%m%d%Y_%H_%M_%S") + "/"
    os.mkdir(save_path)

    processes = [
        mp.Process(target=save_png, args=(save_path, color_img_q, state_dict)),
    ]

    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    while True:
        data = pipeline.wait_for_frames()
        data = align.process(data)
        depth = data.get_depth_frame()
        color = data.get_color_frame()

        depth_image = np.asanyarray(depth.get_data())
        color_image = np.asanyarray(color.get_data())
        depth_image = cv2.flip(depth_image, -1)
        color_image = cv2.flip(color_image, -1)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)
        tname = str(time.time()) + '.png'

        color_img_q.put((color_image, depth_image, tname))
        # print("color_img_q size: ", color_img_q.qsize())
        color_img_q.get() if color_img_q.qsize() > 1 else None

        # Show images
        if show:
            cv2.imshow('images0', np.hstack((color_image, depth_colormap)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


def save_png(save_dir, color_img_q=None, state_dict=None):
    # if color_img_q is None:
    #     return None

    while True:
        while color_img_q.qsize() == 0:
            time.sleep(0.01)
            # print("color_img_q size: ", color_img_q.qsize())
        (color_image, depth_image, tname) = color_img_q.get()

        if state_dict['isSavePNG']:
            cv2.imwrite(save_dir + 'color' + tname, color_image)
            cv2.imwrite(save_dir + 'depth' + tname, depth_image)
            print("image %s saved", 'color', tname)


# 加载数据集中的文件
def save_image_to_h5py(path):
    img_list = []
    label_list = []
    dir_counter = 0
    num_for_test = 0

    for child_dir in os.listdir(path):
        child_path = os.path.join(path, child_dir)
        # print('文件中的子文件名是:\n', child_path)
        # 总共有9个文件夹 第一个文件夹加载10文件 其他文件夹中加载1个文件
        for dir_image in os.listdir(child_path):
            # print('dir_image中图像的名称是:\n', dir_image)
            img = cv2.imread(os.path.join(child_path, dir_image))
            # img =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#单通道，分辨率会下降
            img_list.append(img)
            label_list.append(dir_counter)

            if num_for_test > 10:
                break
            num_for_test = num_for_test + 1

        # 返回的img_list转成了 np.array的格式
        dir_counter += 1

    img_np = np.array(img_list)
    label_np = np.array(label_list)
    print('数据集中原始的标签顺序是:\n', label_np)

    f = h5py.File('hdf5_file.h5', 'w')
    f['image'] = img_np
    f['labels'] = label_np
    f.close()


# save_image_to_h5py('../Dataset/baidu/train_image/train')


# 加载h5py成np的形式
def load_h5py_to_np(path):
    h5_file = h5py.File(path, 'r')
    print('打印一下h5py中有哪些关键字', h5_file.keys())
    permutation = np.random.permutation(len(h5_file['labels']))
    shuffled_image = h5_file['image'][:][permutation, :, :, :]
    shuffled_label = h5_file['labels'][:][permutation]
    print('经过打乱之后数据集中的标签顺序是:\n', shuffled_label, len(h5_file['labels']))
    return shuffled_image, shuffled_label


# images, labels = load_h5py_to_np('hdf5_file.h5')
#
# for i, image in enumerate(images):
#     cv2.imwrite("filename.png", image)


if __name__ == "__main__":
    mp.set_start_method(method='spawn')
    with mp.Manager() as manager:
        state_dict = manager.dict()
        state_dict['isSavePNG'] = False

        app = App(state_dict)
        color_img_q = mp.Queue(maxsize=2)

        if using_realsense:
            get_image(color_img_q, state_dict)
        else:
            get_image_rgb(color_img_q, state_dict)
