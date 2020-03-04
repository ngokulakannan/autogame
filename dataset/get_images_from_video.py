import cv2,os

def get_images(video,output_path='data_files/palm'):
    '''
    Save images from video

    Get every frame and save the configured frame from the video.
    
    Parameters
    -----------
    video - str
        path of the video to be processed

    output_path - str
        path of the output images to be stored
    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path,output_path)
    video_obj= cv2.VideoCapture(video)
    count=0
    file_name_count=455
    success=1
    while success:
        success,frame = video_obj.read();  #read frame from video
        if not success:
            return;
        file_name = output_path + "/frame_"+str(file_name_count)+'.jpg'
        if count%4 == 0: # save every 4th frame
            cv2.imwrite( file_name,frame)
            file_name_count+=1
        count+=1

    video_obj.release()

''' DRIVER CODE TO CHECK THE SCRIPT '''
if __name__ == '__main__':
    get_images('/xxx/xxx/xxx/xxx/xxx/my_video-4.mkv')