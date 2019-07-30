import numpy as np

class Profile:
    import numpy as np
    def __init__(self, name, arr, picture):
        self.name = name
        self.mean_descriptor = np.mean(arr, axis=0)
        self.array = arr
        self.pic = picture
        
        """
        name = string
        arr = numpy array (128 vector) corresponding to picture of face
        
        """
        
        
    def __call__(self, newarr):
        
        self.array = np.vstack((self.array, newarr))
        self.mean_descriptor = np.mean(self.array, axis=0)
    
        """
        newarr = 128 vector numpy array of new picture of person
        
        returns:
            new_mean_descriptor = numpy array
        
        """

# database = {name(string), name(class)}

    