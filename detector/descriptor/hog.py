from skimage import feature

class HOG:
    '''
    Class to store the HOG parameters and extract HOG features from image
    '''
    def __init__(self, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), normalize=True  ):
        self.__orientations = orientations
        self.__pixels_per_cell = pixels_per_cell
        self.__cells_per_block = cells_per_block
        self.__normalize = normalize

    def describe(self,image):
        '''
        Extract the HOG features from given image

        Parameters
        ----------
        image - numpy array
            image for which HOG features to be extracted
        '''
        hog_features=feature.hog(image,self.__orientations,self.__pixels_per_cell,
                    self.__cells_per_block,transform_sqrt=self.__normalize,block_norm='L1')
        return hog_features;

