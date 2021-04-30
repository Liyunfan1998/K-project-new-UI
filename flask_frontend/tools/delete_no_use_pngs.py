import os

# threshold_start = 1619600139.0629585
# threshold_end = 1619600176.6989167
# base_dir = '/home/liyunfan/Desktop/GraduationProject/liyunfan/collect_0428/collect_04282021_16_55_26'
dry_run=True

threshold_start = 1619601146.5541384
threshold_end = 1619601185.3990479
base_dir = '/home/liyunfan/Desktop/GraduationProject/liyunfan/collect_0428/collect_04282021_17_12_18'
video_name = base_dir+'.avi'

count = 0
all = 0
for root, dirs, files in os.walk(base_dir, topdown=False):
    for name in files:
        all+=1
        # print((float)(name[5:-4]))
        if not threshold_start<(float)(name[5:-4])<threshold_end:
            print("remove:", name)
            if not dry_run:
                os.remove(os.path.join(root, name))
            count+=1

print("all:", all)
print("removed:", count)
# Color
# Depth
import cv2

def create_avi_from_png(image_folder = './images', video_name = 'video.avi'):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        float_list = [(float)(name[5:-4]) for name in files if name[0]=='c' and name[-1]=='g']
        float_list.sort()
        images = ['color'+str(flt)+'.png' for flt in float_list]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(video_name, fourcc, 30, (640,480))
        # output_filename, fourcc, fps, self._window_shape
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        cv2.destroyAllWindows()
        video.release()

create_avi_from_png(base_dir,video_name)
