import cv2
from sklearn.svm import SVC
import pickle
import numpy as np 
import os
from detector.configuration.config import get_config
from detector.descriptor.hog import HOG
from multiprocessing import Process, Queue

class detector:
    '''
    Class to detect the palm in the specified boxes.

    Attributes
    ----------
    model : SVM model
        trained model to predict the palm in the image
    hog : HOG Object
        Object holds the HOG parametrs used during training time
    min_probability : float
        minimum probability to be qualify as palm
    window_dim : tuple
        tuple holding the image dimension during trining

    Methods
    -------
    find :  (boxes,frame_queue,control_queue,is_video=True) 
        find whether palm is present or not in the given boxes  
    '''
    def __init__(self):
        config = get_config()
        self.model = pickle.loads( open( os.path.join( config["output_path"] ,"palmar.pickle"  ),'rb').read() )
        self.hog = HOG(pixels_per_cell=config['pixels_per_cell'] , cells_per_block = config['cells_per_block'])
        self.min_probability = config['min_probability']
        self.window_dim = tuple(config['window_dim'])

    

    def find(self,boxes,frame_queue,control_queue,is_video=True):
        '''
        find boxes with palm and sent corresponding controls to other process

        Get the image through the queue from other process and extract the image parts
        at the dimensions of given boxes. find presence of palm in each box location.
        Draw the boxes and send it to main process. find the control name and send it to other process.

        Parameters
        ----------
        boxes - list
            list with dimensions of four bounding boxes
        frame_queue - Queue
            Queue to send/ recieve image frames
        control_queue - Queue
            Queue to send controls
        is_video - bool
            flag for testing
        '''
        while True: #infinite loop
            if not is_video: #for testing
                image = cv2.imread(image)
            else:
                image = frame_queue.get() # get image from another process
            original = image.copy()
            image = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY)
            control_list = []
            found_windows = []
            box_types = ["Accelerate","Stop","Left","Right" ]
            for box_no,box in enumerate( boxes):
                window = image[ box[1]:box[3] , box[0]:box[2]]
                window = cv2.resize(window,self.window_dim)
                features = self.hog.describe(window)
                prob = self.model.predict_proba([features])[0][1]
    
                cv2.rectangle(original,(box[0],box[1]),(box[2],box[3]),(255,155,55),2) # draw the boxes
                
                if prob > self.min_probability :
                    cv2.putText(original,box_types[box_no],(box[0],box[1]-20),
                        cv2.FONT_HERSHEY_COMPLEX,1,  color=(255,0,0),thickness=3) # draw the control text for controls that are found
                    control_list.append( box_types[box_no]  )
                    found_windows.append(window)
                else:
                    cv2.putText(original,box_types[box_no],(box[0],box[1]-20),
                        cv2.FONT_HERSHEY_COMPLEX,.75,  color=(0,0,255),thickness=2) # draw the corresponding control text for controls that are not found
            
            if not is_video:  
                return (original,control_list)
            else:  # return to corresponding processes
                frame_queue.put(original)
                control_queue.put(control_list)
            
            

''' DRIVER CODE TO CHECK THE SCRIPT '''
if __name__ == '__main__':

    boxes = [

                [ 20,110 ,200,380 ],

                [ 220,110 ,400,380 ],

                [ 800,110 ,1000,380 ],

                [ 1050,110 ,1250,380 ]
    ]

    detector_obj = detector()
    (original,control) = detector_obj.find(boxes,'/xxx/xxx/xxx/xxx/xxx/my_photo-9.jpg',false)
    cv2.imshow("image",original)
    cv2.waitKey()