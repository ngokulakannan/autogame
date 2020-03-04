import cv2
import numpy as np 
import os
from configuration.config import get_config
from dataset.annotations import get_annotations
from descriptor.hog import HOG
from dataset.dataset_ops import dataset_ops
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.svm import SVC
import data_store 
import pickle



class trainer:
    '''
    Class to train the model to prdict palm or not

    Attributes
    ----------
    config : dict
        Dictionary which holds information about the 
        configuration from config file
    
    Methods
    -------
    extract_features :  () 
        Extract Featues, train madel and save it to file
        

    '''
    def __init__(self):
        self.config = get_config()


    def extract_features(self):
        '''
        Extract the features of input images at given annotations and write to a file 

        Get all configurations from config dict for HOG object. Get all images from 
        input folder, extract the annotated region and extract HOG features from that.
        Also extrct random regions from negetive images and extract HOG features from that.
        Write these features into a hdf5 file.
        
        '''
        dataset_path = self.config['source_path']
        output_path = self.config['output_path']
        window_dim = tuple(self.config['window_dim'])
        max_distractions = self.config['num_distractions_per_image']
        hog = HOG(pixels_per_cell=self.config['pixels_per_cell'] , cells_per_block = self.config['cells_per_block'] )
        image_names = dataset_ops.get_file_list(dataset_path,False)
        annotations_list = get_annotations()

        palmar = []
        palmar_lables = []

        negetive = []
        negetive_labels=[]

        for image_name in image_names[:30]:
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

        print('Distraction feature extraction Ended... ')
        print('Saving features to file started... ')
        output_file = os.path.join(output_path,'features.hdf5')
        data_store.dump_data(output_file,'palmar',palmar,'a')
        data_store.dump_data(output_file,'palmar_lables',palmar_lables,'a')
        data_store.dump_data(output_file,'negetive',negetive,'a')
        data_store.dump_data(output_file,'negetive_labels',negetive_labels,'a')

        print('Saving features to file ended... ')


    def train(self):
        '''
        Retrieve the features from hdf5 file.
        Train these featues with SVM classifier and write to a file. 
        '''
        output_path = self.config['output_path']
        print('Retrieving features... ')
        output_file = os.path.join(output_path,'features.hdf5')
        palmar = data_store.get_data(output_file , 'palmar')
        palmar_lables = data_store.get_data(output_file , 'palmar_lables')
        negetive = data_store.get_data(output_file , 'negetive')
        negetive_labels = data_store.get_data(output_file , 'negetive_labels')

        print("Training palmar classifier...")
        
        palmar = np.vstack([palmar, negetive])
        palmar_lables = np.hstack([palmar_lables, negetive_labels])

        palmar_model = SVC(kernel="linear", C=self.config['C'] , probability=True, random_state=42)
        palmar_model.fit(palmar, palmar_lables)

        print("Writing palmar classifier to file...")
        palmar_file = os.path.join(output_path,'palmar.pickle')
        with open(palmar_file,'wb') as palmar_pickle:
            palmar_pickle.write( pickle.dumps(palmar_model))

        print("Training Completed...")
        

if __name__ == '__main__':
    training_obj = trainer()
    training_obj.extract_features()
    training_obj.train()





            


