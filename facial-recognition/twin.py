import numpy as np
def search_twin(celebs,database,name):
    '''takes in name and database
    looks through the database for closest descriptor with different name
    returns the name of closest descriptor
    '''
    closest=list(celebs.keys())[0]
    for key in celebs:
        #print(database[key])
        #print(database[name])
        diff1=np.linalg.norm(celebs[closest][1] - database[name][2])
        diff2=np.linalg.norm(celebs[key][1] - database[name][2])
        if diff1>diff2 and key is not name:
            closest=key
    return closest
