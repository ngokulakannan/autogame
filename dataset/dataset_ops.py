import cv2;
import sys
import os
import glob;
import numpy as np;
import pandas as pd
import pickle 


# https://sites.google.com/view/11khands

class dataset_ops:

    def __init__(self,src_dir='dataset/data_files/Hands',dst_dir='dataset/data_files/new_hands',temp_dir='dataset/data_files/temp',data_dir='dataset/data_files'):
        self.__data_dir=data_dir
        self.__src_dir=src_dir
        self.__dst_dir=dst_dir
        self.__temp_dir=temp_dir
        self.__temp_list=[]
        self.__max_file='max.txt'
        self.__pickle_file='data.pickle'

    @staticmethod  
    def get_file_list(src_dir=None, use_current_dir=True, include_path=False):

        if use_current_dir:
            current_dir = os.getcwd()
        else:
            current_dir = ''
        
        data_folder = os.path.join(current_dir, src_dir)
        print(current_dir,src_dir)
        file_list = os.listdir(data_folder)
        if include_path:
            file_list = [ os.path.join(data_folder, file) for file in file_list  ]
        return file_list


    def crop_images(self,src_dir=None, dst_dir=None, temp_dir=None, data_dir=None, use_current_dir=True):
        if src_dir is None:
            src_dir =  self.__src_dir

        if dst_dir is None:
            dst_dir = self.__dst_dir

        if temp_dir is None:
            temp_dir =  self.__temp_dir

        if data_dir is None:
            data_dir = self.__data_dir

        if use_current_dir:
            current_dir = os.getcwd()
        else:
            current_dir = ''
        print(src_dir,dst_dir)
        src_folder = os.path.join(current_dir, src_dir)
        dst_folder = os.path.join(current_dir, dst_dir)
        temp_folder = os.path.join(current_dir, temp_dir)
        file_names = self.get_file_list()
        self.__temp_list=[]
        max_width=0;max_height=0;

        start_1 = pd.Timestamp.now()
        print(start_1,flush=True)

        for file in file_names:
            #file="Hand_0004403.jpg"
            path = os.path.join(src_folder, file);
            #path = os.path.join(src_folder, "Hand_0001469.jpg");#Hand_0000002    Hand_0001469 Hand_0000223 Hand_0004403
            #print('readfile:', path)
            img = cv2.imread(path)
            img = cv2.resize(img, (800,600), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.blur(gray, (10, 10), 0)
            (t, thres_img) = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)
            #(t, thres_img) = cv2.threshold(blur, 0, 255,(cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU))
            #thres_img = cv2.adaptiveThreshold(blur, 255,	cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 3)


            # cv2.imshow('s',thres_img);
            # cv2.waitKey();
            # break
            # thres_img = cv2.dilate(thres_img.copy(), (150, 150), iterations=10)
            # cv2.imshow('s',thres_img);
            #cv2.waitKey();
            (_, contors, _) = cv2.findContours(thres_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            max_contor = 0
            max_area = 0
            for (i, c) in enumerate(contors):
                area = cv2.contourArea(c);
                if area > max_area:
                    max_area=area
                    max_contor=i 

            (x,y,w,h) = cv2.boundingRect(contors[max_contor])
            x1= max(0,x-20)
            y1= max(0,y-20)
            x2= min(img.shape[1], x + w+20)
            y2= min(img.shape[0], y + h+20)

            img_new=img[y1:y2,x1:x2]

            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),5)
            #cv2.drawContours(img, contors, -1, (0, 255, 0), -1)
            
            if(max_width<(x2-x1)):
                max_width=(x2-x1)
            if(max_height<(y2-y1)):
                max_height=(y2-y1)
            
            #img_new = cv2.resize(img_new, (800,600), interpolation=cv2.INTER_AREA)
            temp_file = os.path.join(temp_folder,file);
            dst_file = os.path.join(dst_folder,file);
            self.__temp_list.append((temp_file,dst_file))

            

            
            cv2.imwrite(temp_file,img_new)
        

        
        print(pd.Timestamp.now()-start_1,flush=True)

        with open( os.path.join( data_dir, self.__max_file) ,'w'  ) as file:
            file.write( str(max_width)+' '+ str(max_height))
        print(max_width,max_height)
        
        with open( os.path.join( data_dir, self.__pickle_file) ,'w+b'  ) as file:
            pickle.dump(self, file) 
            


    def make_images(self,data_dir=None):

        if data_dir is None:
            data_dir = self.__data_dir

        start = pd.Timestamp.now()
        print(start,flush=True)

        with open( os.path.join( data_dir, self.__max_file) ,'r'  ) as file:
            data=file.readline()
            data = data.split()
            max_width= int(data[0])
            max_height= int(data[1])

        for file in self.__temp_list:
            img = cv2.imread(file[0])
            mask = np.zeros((max_height+10,max_width+10,3), dtype="uint8")
            mask[:,:,:]=255
            mask[:img.shape[0],:img.shape[1],:]=img
            #img = cv2.resize(img, (max_width,max_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(file[1],mask)
            break
        print(pd.Timestamp.now()-start,flush=True)


    def use_pickle(self,pickle_path='dataset/data_files/data.pickle'):
        with open( pickle_path ,'r+b'  ) as file:
            self= pickle.load(file) 

    
    def find_average(self,path):
        files = self.get_file_list(path)
        total=0
        h_tot=0
        w_tot=0
        
        for file in files:
            file = os.path.join(path , file)
            img = cv2.imread(file)
            (h,w)=img.shape[:2]
            h_tot+=h
            w_tot+=w
            total+=1
        h_avg = h_tot / total
        w_avg = w_tot / total
        print('Average height',h_avg)
        print('Average width',w_avg)
        return (h_avg,w_avg)



# t=dataset_ops()   
# #print(t.get_file_list(src_dir='dataset/data_files/temp'))
# #t.crop_images()
# #t.make_images()
# print( t.find_average('dataset/data_files/temp')      )






