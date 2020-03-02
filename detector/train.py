import cv2
import numpy as np 
import os
import pandas as pd
from configuration.config import get_config
from dataset.annotations import get_annotations
from descriptor.hog import HOG
from dataset.dataset_ops import dataset_ops
from utilities import rotate
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.svm import SVC
import data_store 
import pickle
from detect import detector


class trainer:

    def __init__(self):
        self.config = get_config()


    def extract_features(self):

        dataset_path = self.config['source_path']
        output_path = self.config['output_path']
        window_dim = tuple(self.config['window_dim'])
        max_distractions = self.config['num_distractions_per_image']
        hog = HOG(pixels_per_cell=self.config['pixels_per_cell'] , cells_per_block = self.config['cells_per_block'] )
        image_names = dataset_ops.get_file_list(dataset_path,False)
        annotations_list = get_annotations()

        palmar = []
        palmar_lables = []
        # dorsal = []
        # dorsal_lables = []
        negetive = []
        negetive_labels=[]


        start_1 = pd.Timestamp.now()
        print(start_1)
        for image_name in image_names[:60]:
            try:
                annotation = annotations_list[image_name]
            except KeyError:
                continue
            image = os.path.join(dataset_path,image_name)
            image = cv2.imread(image)
            grey =  cv2.cvtColor( image, cv2.COLOR_BGR2GRAY)
            grey =  grey[annotation[1]:annotation[3] , annotation[0]:annotation[2]]
            img = cv2.resize(grey, window_dim)
            

            
            features = hog.describe(img)

            palmar.append(features)
            palmar_lables.append(1)
        
        
        start_2 = pd.Timestamp.now()
        print('Images feature extraction Ended ',  start_2-start_1)
        print('Distraction extraction started ', start_2)
        image_distractions = self.config['image_distractions']
        distraction_names = dataset_ops.get_file_list(image_distractions,False)  
        for image in distraction_names:
            image = os .path.join(image_distractions,image)
            image = cv2.imread(image)
            grey =  cv2.cvtColor( image, cv2.COLOR_BGR2GRAY) 
            patches = extract_patches_2d(grey,window_dim,max_patches=max_distractions)

            for img in patches:
                features = hog.describe(img)
                negetive.append(features)
                negetive_labels.append(-1)

        

        start_3 = pd.Timestamp.now()
        print('Distraction feature extraction Ended ',  start_3-start_2)
        print('Saving to file started ', start_3)
        output_file = os.path.join(output_path,'features.hdf5')
        # data_store.dump_data(output_file,'dorsal',dorsal)
        # data_store.dump_data(output_file,'dorsal_lables',dorsal_lables,'a')
        data_store.dump_data(output_file,'palmar',palmar,'a')
        data_store.dump_data(output_file,'palmar_lables',palmar_lables,'a')
        data_store.dump_data(output_file,'negetive',negetive,'a')
        data_store.dump_data(output_file,'negetive_labels',negetive_labels,'a')

        start_4 = pd.Timestamp.now()
        print('Saving to file ended ', start_4-start_3)


    def train(self,do_hard_negetive=False):
        output_path = self.config['output_path']
        start_1 = pd.Timestamp.now()
        print('Retrieving features ',start_1)
        output_file = os.path.join(output_path,'features.hdf5')
        # dorsal = data_store.get_data(output_file , 'dorsal')
        # dorsal_lables = data_store.get_data(output_file , 'dorsal_lables')
        palmar = data_store.get_data(output_file , 'palmar')
        palmar_lables = data_store.get_data(output_file , 'palmar_lables')
        negetive = data_store.get_data(output_file , 'negetive')
        negetive_labels = data_store.get_data(output_file , 'negetive_labels')

        if(do_hard_negetive):
            hard_negetive = data_store.get_data(output_file , 'negetive')
            hard_negetive_labels = data_store.get_data(output_file , 'negetive_labels')


        start_2 = pd.Timestamp.now()
        print("Training dorsal classifier...",start_2)
        
        # dorsal = np.vstack([dorsal, negetive]) 
        # dorsal_lables = np.hstack([dorsal_lables, negetive_labels])
        # dorsal_model = SVC(kernel="linear", C=self.config['C'], probability=True, random_state=42)
        # dorsal_model.fit(dorsal, dorsal_lables)

        # start_3 = pd.Timestamp.now()
        # print("Writing dorsal classifier to file...",start_3)
        # dorsal_file = os.path.join(output_path,'dorsal.pickle')
        # with open(dorsal_file,'wb') as dorsal_pickle:
        #     dorsal_pickle.write( pickle.dumps(dorsal_model))
        
        start_4 = pd.Timestamp.now()
        print("Training palmar classifier...",start_4)
        
        palmar = np.vstack([palmar, negetive])
        palmar_lables = np.hstack([palmar_lables, negetive_labels])
        if(do_hard_negetive):
            palmar = np.vstack([palmar, hard_negetive])
            palmar_lables = np.hstack([palmar_lables, hard_negetive_labels])
        palmar_model = SVC(kernel="linear", C=self.config['C'] , probability=True, random_state=42)
        palmar_model.fit(palmar, palmar_lables)

        start_5 = pd.Timestamp.now()
        print("Writing palmar classifier to file...",start_5)
        palmar_file = os.path.join(output_path,'palmar.pickle')
        with open(palmar_file,'wb') as palmar_pickle:
            palmar_pickle.write( pickle.dumps(palmar_model))

        start_6 = pd.Timestamp.now()
        print("Training Completed...",start_6)
        #self.dorsal_model=dorsal_model
        self.palmar_model=palmar_model

    def hard_negetive_mining(self):
        output_path = self.config['output_path']
        start_1 = pd.Timestamp.now()
        print('Retrieving features ',start_1)
        output_file = os.path.join(output_path,'features.hdf5')
        window_dim = tuple(self.config['window_dim'])
        model = pickle.loads( open( os.path.join( self.config["output_path"] ,"palmar.pickle"  ),'rb').read() )
        hog = HOG(pixels_per_cell=self.config['pixels_per_cell'] , cells_per_block = self.config['cells_per_block'] )
        #model = self.palmar_model
        obj_detector = detector(model,hog)

        image_distractions = self.config['image_distractions']
        distraction_names = dataset_ops.get_file_list(image_distractions,False)  

        negetive = []
        negetive_labels=[]
        mis_found = []

        for image in distraction_names:
            image = os .path.join(image_distractions,image)
            image = cv2.imread(image)
            grey =  cv2.cvtColor( image, cv2.COLOR_BGR2GRAY)

            (boxes,prob_list) = obj_detector.detect(image)


            boxes = np.array(boxes)
            prob_list = np.array(prob_list)
            boxes = obj_detector.non_max_suppression(boxes, prob_list, self.config['overlap_thresh'])
            mis_found = []
            for box in boxes : 
                #print(  image.shape )
                #print(   box[0],box[2] , box[1],box[3] )
                img = cv2.resize(grey[  box[1]:box[3]  ,   box[0]:box[2] ], window_dim)
                mis_found.append( img )

        for img in mis_found:
            features = hog.describe(img)
            negetive.append(features)
            negetive_labels.append(-1) 

        data_store.dump_data(output_file,'hard_negetive',negetive,'a')
        data_store.dump_data(output_file,'hard_negetive_labels',negetive_labels,'a')
                


    # def load_model(path):
    #     palmar_file = os.path.join(path,'palmar.pickle')
    #     dorsal_file = os.path.join(path,'dorsal.pickle')

        



train_obj = trainer()
train_obj.extract_features()
train_obj.train()
#train_obj.hard_negetive_mining()
#train_obj.train(True)




            


