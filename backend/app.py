from flask import Flask,request,jsonify,send_file,url_for
from flask_cors import CORS
import base64
from PIL import Image
import requests
from threading import Thread
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from load_resnet import resnetPredict
#from app4_rn import predict_image_classification_sample 

app = Flask(__name__)
CORS(app)
#resnet,ensemble1,ensemble2...
endpoints = {
	'resnet': 'models/resnetModel17.h5',
	'ensemble1' : 'models/base_learner_0.h5',
	'ensemble2' : 'models/base_learner_1.h5',
	'ensemble3' : 'models/base_learner_2.h5',
}

def getList(id):
    print(endpoints[id])
    if id == 'resnet':
        l=resnetPredict(endpoints[id],"garbage.jpeg")
        print(l)
        [non, clean, dirty] = l.tolist()[0]
        return [clean, dirty, non]
    else:
        model = load_model(endpoints[id])
        input_arr = img_to_array(load_img("garbage.jpeg"))
        input_arr = input_arr.reshape((1,) + input_arr.shape)
        input_arr = tf.image.resize(input_arr, [200, 200], method='nearest')
        test=model.predict(input_arr)
        print(test)
        return test.tolist()[0]

def process_id(id, store=None) :
    if store is None:
        store = {}
    store[id] = getList(id)
    #store[id]=predict_image_classification_sample(
    #project="320940575449",
    #endpoint_id=endpoints[id],
	#filename='garbage.jpg',
    #location="asia-southeast1"
    #)

def threaded_process_range():
    """process the id range in a specified number of threads"""
    store = {}
    threads = []
    # create the threads
    for id in endpoints.keys():
        t = Thread(target=process_id, args=(id,store))
        threads.append(t)

    # start the threads
    [ t.start() for t in threads ]
    # wait for the threads to finish
    [ t.join() for t in threads ]
    return store

@app.route("/classification",methods = ["POST"])
def classification():
    req = request.get_json(silent=False, force=True)
    photo = req['photo']
    image=open('garbage.jpeg','wb')
    image.write(base64.b64decode(photo.split(',')[1]))
    image.close()
    store = threaded_process_range()
    ensemble = [0, 0, 0]
    classification = ["clean recyclables", "dirty recyclables", "non recyclables"]
    resnet = [0, 0, 0]
    getResnet = False
    for i in store.keys():
        if i == 'resnet':
            resnet = store[i]
            #print("get resnet, resnet", resnet)
            getResnet = True
        else:
            #print(i, store[i])
            ensemble[0] += store[i][0]
            ensemble[1] += store[i][1]
            ensemble[2] += store[i][2]
    ensembleNum = sum(ensemble)
    ensemble = [i/ensembleNum for i in ensemble]
    print("ensemble", ensemble)
    print("resnet", resnet)
    average = [0, 0, 0]
    if getResnet:
        average = [(resnet[i] + ensemble[i]) / 2 for i in range(3)]
    else:
        average = ensemble
    res = classification[np.argmax(average)]
    print(res)
    
    return jsonify(res)
    #classification = ["clean recyclables", "dirty recyclables", "non recyclables"]
    #return jsonify(classification[np.argmax(res)])

if __name__ == '__main__':
    #app.run(host="192.168.43.49", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
# flask run --host=0.0.0.0