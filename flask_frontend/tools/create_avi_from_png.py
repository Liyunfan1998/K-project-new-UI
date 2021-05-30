import cv2
import os


def create_avi_from_png(image_folder='images', video_name='video.avi'):
    for root, dirs, files in os.walk(image_folder, topdown=False):
        float_list = [(float)(name[5:-4]) for name in files if name[0] == 'c' and name[-1] == 'g']
        float_list.sort()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        images = ['color' + str(flt) + '.png' for flt in float_list]
        video = cv2.VideoWriter(video_name, fourcc, 25, (640, 480))
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        cv2.destroyAllWindows()
        video.release()


# create_avi_from_png('collect_0424/collect_04242021_16_21_27', 'collect_04242021_16_21_27.avi')
# create_avi_from_png('collect_0428/collect_04282021_17_12_18', 'collect_04282021_17_12_18.avi')
# create_avi_from_png('collect_0421/collect_04212021_18_13_21', 'collect_04212021_18_13_21.avi')
create_avi_from_png('collect_0421/collect_04212021_18_07_25', 'collect_04212021_18_07_25.avi')
