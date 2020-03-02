import cv2
from sklearn.svm import SVC
import pickle
import numpy as np 
import os
import pandas as pd
from detector.configuration.config import get_config
from detector.descriptor.hog import HOG
from multiprocessing import Process, Queue , Lock
import gameControls.controls as controls

class detector:
    def __init__(self):
        config = get_config()
        self.model = pickle.loads( open( os.path.join( config["output_path"] ,"palmar.pickle"  ),'rb').read() )
        self.hog = HOG(pixels_per_cell=config['pixels_per_cell'] , cells_per_block = config['cells_per_block'])
        self.min_probability = config['min_probability']
        self.window_dim = tuple(config['window_dim'])

    

    def find(self,boxes,frame_queue,control_queue,is_video=True):

        while True:
            if not is_video:
                image = cv2.imread(image)
            else:
                image = frame_queue.get()
            original = image.copy()
            image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY)
            control_list = []
            found_windows = []
            box_types = ["Accelerate","Stop","Left","Right" ]
            for box_no,box in enumerate( boxes):
                window = image[ 110:350 , 20:170]
                window = image[ box[1]:box[3] , box[0]:box[2]]
                window = cv2.resize(window,self.window_dim)
                features = self.hog.describe(window)
                prob = self.model.predict_proba([features])[0][1]
    
                cv2.rectangle(original,(box[0],box[1]),(box[2],box[3]),(255,155,55),2)
                
                if prob > self.min_probability :
                    cv2.putText(original,box_types[box_no],(box[0],box[1]-20), cv2.FONT_HERSHEY_COMPLEX,1,  color=(255,0,0),thickness=3)
                    control_list.append( box_types[box_no]  )
                    found_windows.append(window)
                else:
                    cv2.putText(original,box_types[box_no],(box[0],box[1]-20), cv2.FONT_HERSHEY_COMPLEX,.75,  color=(0,0,255),thickness=2)
                
            frame_queue.put(original)
            control_queue.put(control_list)
            
            


if __name__ == '__main__':

    boxes = [

                [ 20,110 ,200,380 ],

                [ 220,110 ,400,380 ],

                [ 800,110 ,1000,380 ],

                [ 1050,110 ,1250,380 ]

    ]

    detector_obj = detector()
    (original,control) = detector_obj.find(boxes,'/home/gokul/snap/guvcview/81/my_photo-9.jpg',false)
    cv2.imshow("image",original)
    cv2.waitKey()