from portfolio_methods import create_profile
from camera import take_picture
import pickle
import numpy as np
from dlib_models import download_model, download_predictor, load_dlib_models
from dlib_models import models
import matplotlib.pyplot as plt
from celeb_profile import create_celeb

def create_celeb(image_path):
    # with open("image_arrays.pkl", mode="rb") as opened_file:
    #     image_arrays = pickle.load(opened_file)

    download_model()
    download_predictor()
    load_dlib_models()
    img_arr = plt.imread(image_path,format='jpg').copy()
    face_detect = models["face detect"]
    face_rec_model = models["face rec"]
    shape_predictor = models["shape predict"]
    detections = list(face_detect(img_arr))
    #fig, ax = plt.subplots()
    #ax.imshow(img_arr)
    print("Number of faces detected: {}".format(len(detections)))
    for face in detections:
        # let's take a look as to what the descriptor is!!
        shape = shape_predictor(img_arr, face)
        descriptor = np.array(face_rec_model.compute_face_descriptor(img_arr, shape))
        return descriptor
    # add_profile = input("Would you like to add this picture to the database? [y/n]  ")
    # if add_profile == "y":
    #     new_name = input(f"What is the celebrity's name?   ")
        image_arrays = create_celeb(img_arr, descriptor, new_name, image_arrays)
    # with open("image_arrays.pkl", mode="wb") as opened_file:
    #     pickle.dump(image_arrays, opened_file)


if __name__ == '__main__':
    create_celeb()