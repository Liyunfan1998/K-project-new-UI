from yolov5 import YOLOv5
import numpy as np

# set model params
model_path = "yolov5/weights/yolov5s.pt"  # it automatically downloads yolov5s model to given path
device = "cuda"  # or "cpu"

# init yolov5 model
yolov5 = YOLOv5(model_path, device)

# load images
image1 = 'https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg'
image2 = 'https://github.com/ultralytics/yolov5/blob/master/data/images/bus.jpg'

# perform inference
results = yolov5.predict(image1)
"""
# perform inference with larger input size
results = yolov5.predict(image1, size=1280)

# perform inference with test time augmentation
results = yolov5.predict(image1, augment=True)

# perform inference on multiple images
results = yolov5.predict([image1, image2], size=1280, augment=True)
"""
# print(results)
# show detection bounding boxes on image
# results.show()

# save results into "results/" folder
# results.save(save_dir='results/')

print(results.pred)
# print(results.pred[0])
# print(np.array(results.pred[0].cpu(), dtype=int))


coco_class_names = {0: u'__background__',
                    1: u'person',
                    2: u'bicycle',
                    3: u'car',
                    4: u'motorcycle',
                    5: u'airplane',
                    6: u'bus',
                    7: u'train',
                    8: u'truck',
                    9: u'boat',
                    10: u'traffic light',
                    11: u'fire hydrant',
                    12: u'stop sign',
                    13: u'parking meter',
                    14: u'bench',
                    15: u'bird',
                    16: u'cat',
                    17: u'dog',
                    18: u'horse',
                    19: u'sheep',
                    20: u'cow',
                    21: u'elephant',
                    22: u'bear',
                    23: u'zebra',
                    24: u'giraffe',
                    25: u'backpack',
                    26: u'umbrella',
                    27: u'handbag',
                    28: u'tie',
                    29: u'suitcase',
                    30: u'frisbee',
                    31: u'skis',
                    32: u'snowboard',
                    33: u'sports ball',
                    34: u'kite',
                    35: u'baseball bat',
                    36: u'baseball glove',
                    37: u'skateboard',
                    38: u'surfboard',
                    39: u'tennis racket',
                    40: u'bottle',
                    41: u'wine glass',
                    42: u'cup',
                    43: u'fork',
                    44: u'knife',
                    45: u'spoon',
                    46: u'bowl',
                    47: u'banana',
                    48: u'apple',
                    49: u'sandwich',
                    50: u'orange',
                    51: u'broccoli',
                    52: u'carrot',
                    53: u'hot dog',
                    54: u'pizza',
                    55: u'donut',
                    56: u'cake',
                    57: u'chair',
                    58: u'couch',
                    59: u'potted plant',
                    60: u'bed',
                    61: u'dining table',
                    62: u'toilet',
                    63: u'tv',
                    64: u'laptop',
                    65: u'mouse',
                    66: u'remote',
                    67: u'keyboard',
                    68: u'cell phone',
                    69: u'microwave',
                    70: u'oven',
                    71: u'toaster',
                    72: u'sink',
                    73: u'refrigerator',
                    74: u'book',
                    75: u'clock',
                    76: u'vase',
                    77: u'scissors',
                    78: u'teddy bear',
                    79: u'hair drier',
                    80: u'toothbrush'}
