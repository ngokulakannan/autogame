import cv2,os

def get_images(video,output_path='data_files/palm'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path,output_path)
    video_obj= cv2.VideoCapture(video)
    count=0
    file_name_count=455
    success=1
    while success:
        success,frame = video_obj.read();
        if not success:
            return;
        file_name = output_path + "/frame_"+str(file_name_count)+'.jpg'
        if count%4 == 0:
            cv2.imwrite( file_name,frame)
            file_name_count+=1
        count+=1

    video_obj.release()

get_images('/home/gokul/snap/guvcview/81/my_video-4.mkv')