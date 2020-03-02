import cv2
import numpy as np
import detector.detect as detect
import gameControls.controls as controls
from multiprocessing import Process, Queue , Lock

detector_obj = detect.detector()
video_obj= cv2.VideoCapture(0)
video_obj.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video_obj.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
count=0
success=1
boxes = [ [ 20,110 ,200,380 ], [ 220,110 ,400,380 ], [ 800,110 ,1000,380 ], [ 1050,110 ,1250,380 ] ]

control_queue = Queue()
frame_queue = Queue()
detector_process = Process(target=detector_obj.find,args=(boxes,frame_queue,control_queue))
detector_process.daemon = True
detector_process.start()


control_process = Process(target=controls.move_vehicle,args=(control_queue,))
control_process.daemon = True
control_process.start()

while success:
    success,frame = video_obj.read();
    flipped_frame = cv2.flip( frame,1)
    #(original,control_list) = detector_obj.find(boxes, flipped_frame)
    frame_queue.put_nowait(flipped_frame)
    original = frame_queue.get()
    original = cv2.resize(original,(500,600))
    cv2.imshow("image",original)
    cv2.waitKey(25)
    

video_obj.release()