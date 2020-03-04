import h5py
import numpy as np

def dump_data(file,dataset,data,mode='w'):
    '''
    Create dataset and dump given data in h5py file

    Parameters
    -----------
    file - str
        path of the h5py file

    dataset - str
        name of the dataset

    data - numpy array or int
        data to be dumped

    mode - str, optional
        file mode - 'w' or 'a'
    '''
    db = h5py.File(file,mode=mode)
    data_len = 1 if(type(data[0]) == int) else len(data[0])
    data_set = db.create_dataset(dataset,(len(data),data_len),dtype='float',data=data)
    db.close()

def get_data(file,dataset):
    '''
    Open h5py file and read given dataset and return the data

    Parameters
    -----------
    file - str
        path of the h5py file

    dataset - str
        name of the dataset
    '''
    db = h5py.File(file,mode='r')
    data = db[dataset][()]
    if data.shape[1] == 1: 
        data =  np.resize( data , (data.shape[0],))
    db.close()
    return data


''' DRIVER CODE TO CHECK THE SCRIPT '''
if __name__ == '__main__':
    data = [ 
                [0,1,2],
                [3,1,0],
                [4,3,2],
                [2,1,5],
            ]

    file = '/xxx/xxx/xxx/xxx/xxx/autogame/dataset/test.hdf5'
    dump_data(file,'testds',data)
    d=get_data(file,'testds')
    print( d[:]  )