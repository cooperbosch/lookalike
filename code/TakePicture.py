import matplotlib.pyplot as plt
from camera import take_picture
import numpy as np
import dlib_models
from dlib_models import download_model, download_predictor, load_dlib_models

download_model()
download_predictor()
load_dlib_models()
from dlib_models import models

face_detect = models["face detect"]
face_rec_model = models["face rec"]
shape_predictor = models["shape predict"]


def take_pic():
    pic = take_picture()

    return pic


def get_descriptor(pic):
    load_dlib_models()
    detections = list(face_detect(pic))
    des = []
    for i in range(len(detections)):
        shape = shape_predictor(pic, detections[i])
        descriptor = np.array(face_rec_model.compute_face_descriptor(pic, shape))
        des.append(descriptor / np.linalg.norm(descriptor))
    return des


def find_rectangles(pic):
    detections = list(face_detect(pic))
    rectangles = []
    for i in range(len(detections)):
        r = []
        r.append(detections[i].left())
        r.append(detections[i].top())
        r.append(detections[i].right() - detections[i].left())
        r.append(detections[i].bottom() - detections[i].top())
        rectangles.append(r)

    # to plot rectangles use the following code:
    """
    for r in rectangles:
        rect = Rectangle((r[0], r[1]), r[2], r[3], linewidth=1, edgecolor='r', facecolor='none')

        ax.add_patch(rect)
    """

    return rectangles
