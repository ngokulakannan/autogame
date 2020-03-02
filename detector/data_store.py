import h5py
import numpy as np

def dump_data(file,dataset,data,mode='w'):
    db = h5py.File(file,mode=mode)
    data_len = 1 if(type(data[0]) == int) else len(data[0])
    data_set = db.create_dataset(dataset,(len(data),data_len),dtype='float',data=data)
    db.close()

def get_data(file,dataset):
    db = h5py.File(file,mode='r')
    print('-------------------------------',db.keys())
    data = db[dataset][()]
    if data.shape[1] == 1:
        data =  np.resize( data , (data.shape[0],))
    db.close()
    return data


''' DRIVER CODE TO CHECK THE SCRIPT '''
# data = [ 
#             [0,1,2],
#             [3,1,0],
#             [4,3,2],
#             [2,1,5],
#         ]
# data = [
#     [0],[1],[2],[3]
# ]
# #print(data.shape)
# file = '/media/gokul/my_data/Projects/python/autogame/dataset/test.hdf5'
# dump_data(file,'testds',data)
# d=get_data(file,'testds')
# print( d[:]  )