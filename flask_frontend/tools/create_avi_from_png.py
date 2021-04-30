import cv2

def create_avi_from_png(image_folder = 'images', video_name = 'video.avi'):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        float_list = [(float)(name[5:-4]) for name in files if name[0]=='c' and name[-1]='g']
        float_list.sort()
        images = ['color'+flt+'.png' for flt in float_list]
        video = cv2.VideoWriter(video_name, 0, 1, (640,480))
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
        cv2.destroyAllWindows()
        video.release()
