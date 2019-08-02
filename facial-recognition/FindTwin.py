from flask import Flask
from flask_ask import Ask, statement, question
from flask_ask.models import _Response
app = Flask(__name__)
ask = Ask(app, '/')
#from camera import take_picture
#import matplotlib as plt
from main import main
import matplotlib.pyplot as plt
from camera import take_picture
import numpy as np
import portfolio_methods as portfolio
import match
import pickle
import upload_image
from twin import search_twin
import threading

# run this cell to download the models from dlib
from dlib_models import download_model, download_predictor, load_dlib_models
from dlib_models import models
from camera import take_picture
import matplotlib.pyplot as plt


with open("image_arrays.pkl", mode="rb") as opened_file:
    image_arrays = pickle.load(opened_file)
with open("database.pkl", mode="rb") as opened_file:
    database = pickle.load(opened_file)
    #print(database["Alex"])
    #print([k for k in database])
desc=None
dbname=None

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like me to take your photo?'
    download_model()
    download_predictor()
    load_dlib_models()
    return question(welcome_message)


@ask.intent("YesIntent")
def yes_intent():
    global desc
    global dbname
    name, desc = main(database)
    #print("Desc",desc.shape )
    if "Unknown" not in name:
        face_msg = 'Hello {}'.format(name)
        dbname=name
        return question(face_msg+". Say 'Who do I look like' to see your celebrity look-alike!")
    else:
        return question("What is your name?")


@ask.intent("NameIntent")
def assign_name(name,uk,german,cogworks):
    global database
    global desc
    global dbname
    #print("Desc2", desc.shape)

    if name is not None:
        dbname=name
    elif cogworks is not None:
        dbname=cogworks
    elif uk is not None:
        dbname=uk
    elif german is not None:
        dbname=german

    #print(name,uk,german,cogworks)
    database = portfolio.create_profile(desc, dbname, database)
    face_msg = 'Hello {}'.format(dbname)
    return question(face_msg + ". Say 'Who do I look like' to see your celebrity look-alike!")

@ask.intent("TwinIntent")
def twin_intent():
    global database
    global dbname
    twin_name=search_twin(image_arrays,database,dbname)
    #print(database[twin_name])
    filepath=image_arrays[twin_name][2]
    url=upload_image.upload(filepath)
    res=_Response(speech=twin_name+". Do you want to try again?")
    res._response['shouldEndSession'] = False
    res.standard_card(large_image_url=url)
    return res
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Okay, goodbye'
    with open("database.pkl", mode="wb") as opened_file:
        pickle.dump(database,opened_file)

    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)