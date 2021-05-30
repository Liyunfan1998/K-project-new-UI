import cv2
import os.path
import glob
import numpy as np
from PIL import Image

def convertPNG(pngfile,outdir):
    # READ THE DEPTH
    im_depth = cv2.imread(pngfile)
    #apply colormap on deoth image(image must be converted to 8-bit per pixel first)
    im_color=cv2.applyColorMap(cv2.convertScaleAbs(im_depth,alpha=15),cv2.COLORMAP_JET)
    #convert to mat png
    im=Image.fromarray(im_color)
    #save image
    im.save(os.path.join(outdir,os.path.basename(pngfile)))

for pngfile in glob.glob("/home/liyunfan/Desktop/GraduationProject/K-project-new-UI/flask_frontend/tools/collect_0424/collect_04242021_16_28_00/depth*.png"):#C:/Users/BAMBOO/Desktop/source pics/rgbd_6/depth/*.png
    convertPNG(pngfile,"/home/liyunfan/Desktop/GraduationProject/K-project-new-UI/flask_frontend/tools/collect_0424/collect_04242021_16_28_00/depth_fake")#C:/Users/BAMBOO/Desktop/source pics/rgbd_6/color
