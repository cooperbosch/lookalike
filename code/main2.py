import database
from node import *
from whispers import *

import TakePicture
from matplotlib.patches import Rectangle
from matplotlib import pyplot as plt
import numpy as np
import os.path
import pickle
from database import *

"""
#take picture
@ -38,15 +42,74 @@ for k, d in enumerate(detections):
#ask user if they want to add to database
"""
th = 0.36
font = {"color": "white"}
db = None

def main():
    th = 0.36
    font = {"color": "white"}
    db = None
    print('made db')
    if os.path.exists("database.dict"):
        try:
            savefile = open("database.dict", "rb")
            db = pickle.load(savefile)
            savefile.close()
        except:
            db = dict()
    else:
        db = dict()
        print("made new db")

    # clear_name(db,'emily')
    mode = input("Press 0 to match faces, 1 to enter to database, 2 to find your lookalike")
    if mode == 'q':
        exit()
    mode = int(mode)
    if mode == 0:
        while True:
            find_match()

    elif mode == 1:
        while True:
            add_database()


    elif mode == 2:
        while True:
            find_lookalike()


def find_match():
    a = input("take picture?\n")
    if a == 'q':
        exit()
    if a == 'o':
        main()
    else:

        picture = TakePicture.take_pic()
        fig, ax = plt.subplots()
        rectangles = TakePicture.find_rectangles(picture)

        for r in rectangles:
            rect = Rectangle(
                (r[0], r[1]),
                r[2],
                r[3],
                linewidth=1,
                edgecolor="r",
                facecolor="none",
            )

            ax.add_patch(rect)
        ax.imshow(picture)

        ds = TakePicture.get_descriptor(picture)

        for ind, d in enumerate(ds):
            r = rectangles[ind]
            name = match_face(d, db, th)

            plt.text(r[0] + 40, r[1] + 30, name, fontdict=font)
            # if name == 'unknown':
            # unknowns.append(ind)
            # else:
            # db[name](ds[ind])

        plt.show()

def add_database():
    a = input("take picture?\n")
    if a == 'q':
        exit()
    if a == 'o':
        main()
    else:
        picture = TakePicture.take_pic()
        fig, ax = plt.subplots()
        rectangles = TakePicture.find_rectangles(picture)
        ds = TakePicture.get_descriptor(picture)
        unknowns = list()
        all_indices = list()

        for ind, d in enumerate(ds):
            r = rectangles[ind]
            fig, ax = plt.subplots()
            ax.imshow(picture)
            rect = Rectangle(
                (r[0], r[1]),
                r[2],
                r[3],
                linewidth=1,
                edgecolor="y",
                facecolor="none",
            )
            ax.add_patch(rect)
            name = match_face(d, db, th)

            plt.text(
                r[0], r[1] + r[3] + 40, "Enter name into console", fontdict=font
            )
            plt.show()
            newname = input("Who was that?\n (leave empty to not add)")
            if len(newname) > 0:
                name = newname
                desc = ds[ind]
                if newname in db:
                    db[newname](desc)
                else:
                    db[newname] = Profile(newname, np.array([desc]), picture)
            setpicture = input("Set as profile picture? \n (leave empty for no)")
            if len(setpicture) > 0:
                db[name].pic = picture

        savefile = open("database.dict", "wb")
        pickle.dump(db, savefile)
        savefile.close()


def find_lookalike():
    a = input("take picture?\n")
    if a == 'q':
        exit()
    if a == 'o':
        main()
    else:
        picture = TakePicture.take_pic()
        fig, ax = plt.subplots()
        rectangles = TakePicture.find_rectangles(picture)

        ds = TakePicture.get_descriptor(picture)

        for ind, d in enumerate(ds):
            r = rectangles[ind]
            fig, ax = plt.subplots()
            ax.imshow(picture)
            rect = Rectangle(
                (r[0], r[1]),
                r[2],
                r[3],
                linewidth=1,
                edgecolor="y",
                facecolor="none",
            )
            ax.add_patch(rect)

            plt.text(r[0], r[1] + r[3] + 40, "Use this face?", fontdict=font)
            plt.show()
            selector = input("Use this face?\n (leave empty for no)")
            if len(selector) > 0:
                descriptor = TakePicture.get_descriptor(picture)
                minval = 999
                minkey = "unknown"
                name = match_face(descriptor, db, th)
                for key, d in db.items():

                    dist = np.linalg.norm(d.mean_descriptor - descriptor)
                    if dist < minval and name != key:
                        minval = dist
                        minkey = key
                print("You are " + name + " and you look like " + minkey)
            ax.imshow(db[minkey].pic)
            plt.show()


def clear_name(db, name):
    del db[name]
    savefile = open("database.dict", "wb")
    pickle.dump(db, savefile)
    savefile.close()
    exit(0)


def match_face(descriptor, db, th):
    minval = 999
    minkey = "unknown"
    for name, d in db.items():

        dist = np.linalg.norm(d.mean_descriptor - descriptor)
        if dist < th:
            if dist < minval:
                minval = dist
                minkey = name

    return minkey


if __name__ == "__main__":
    main()
