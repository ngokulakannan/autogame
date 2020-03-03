import os, glob,xml.dom.minidom as dom
from dataset.dataset_ops import dataset_ops


def get_annotations(path='dataset/data_files/annotations/'):
    '''
    Parse the annotation xml files in PASCAL VOC format and return list of bounding boxes

    Get the annotations folder and read all files from the folder.
    Parse each file and retreve the xmin,ymin , xmax, ymax values and append it to a dictionary.
    return that dictionary

    Parameters
    -----------
    path: str
        path of the annotations directory

    '''

    files = dataset_ops.get_file_list(path,include_path=True)
    
    annotation_list ={}
    for file in files:
        doc = dom.parse(file)
        filename = doc.getElementsByTagName('filename')[0].firstChild.data
        xmin = int ( doc.getElementsByTagName('xmin')[0].firstChild.data )
        ymin = int ( doc.getElementsByTagName('ymin')[0].firstChild.data )
        xmax = int ( doc.getElementsByTagName('xmax')[0].firstChild.data )
        ymax = int ( doc.getElementsByTagName('ymax')[0].firstChild.data )

        annotation_list[ filename] = [ xmin,ymin , xmax, ymax  ]
    
    return annotation_list

def find_average_dimensions():
    '''
    Find the average dimensions of dataset

    Get the co-ordinate information of the dataset using get_annotations function.
    Calculate height and width of each box and finally calulate and return the averge dimensions.
    '''

    annotation_list = get_annotations()
    width,height = 0,0
    for value in annotation_list.values():
        width += value[2] - value[0]
        height += value[3] - value[1]
    width = int( width/ len(annotation_list) )
    height = int( height/ len(annotation_list) )

    return (width,height)
 
''' DRIVER CODE TO CHECK THE SCRIPT '''
if __name__ == '__main__':
    a_list = get_annotations()
    for key,value in a_list.items():
        print(key, value)
        break;
    print( find_average_dimensions() )

