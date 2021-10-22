import cv2
from sklearn.cluster import MiniBatchKMeans
import numpy as np

from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image as p_img

import pickle

open_kmeans = open("./data/pickle/kmeans_cv_sift","rb")
kmeans=pickle.load(open_kmeans)
open_kmeans.close()

sift = cv2.SIFT_create(500)

def transform_image(img_path : str):
    image = cv2.imread(img_path,0) # convert in gray
    image = cv2.blur(image,(5,5)) # Filter blur image
    res = cv2.equalizeHist(image)   # equalize image histogram
    return sift.detectAndCompute(res, None)

def get_transform_image(img_path : str):
    image = cv2.imread(img_path,0) # convert in gray
    image = cv2.blur(image,(5,5)) # Filter blur image
    res = cv2.equalizeHist(image)   # equalize image histogram
    return res

def preprocess_1_image(path):
    _,des = transform_image(path)
    return np.asarray([build_histogram(kmeans,des,0)])

def preprocess_multiple_image(list_path):
    all_hist = []
    for path in list_path:
        _,des = transform_image(path)
        all_hist.append(build_histogram(kmeans,des,0))
    return np.asarray(all_hist)

def build_histogram(kmeans, des, image_num):
    res = kmeans.predict(des)
    hist = np.zeros(len(kmeans.cluster_centers_))
    nb_des=len(des)
    if nb_des==0 : print("problème histogramme image  : ", image_num)
    for i in res:
        hist[i] += 1.0/nb_des # pondération par rapport au nombre de descripteur
    return hist

def get_classement_classifier_linear(model,X):
    pred = model.predict_proba(X)
    label = model.classes_
    for i in pred.argsort()[0][::-1]:
        print("#"+str(label[i]),":",str(round(pred[0][i]*100,2))+"%")
        
        
def preprocess_img(path):
    return p_img.img_to_array(p_img.load_img(path,target_size=(224,224)))

def get_image_preprocess(path):
    return preprocess_input(p_img.img_to_array(p_img.load_img(path,target_size=(224,224))))

def preprocess_label(label):
    dic = {
        "food":0,
        "menu":1,
        "drink":2,
        "interior":3,
        "outside":4
    }
    return dic[label]

def get_label(neurone_i):
    dic = {
        0:"food",
        1:"menu",
        2:"drink",
        3:"interior",
        4:"outside"
    }
    return dic[neurone_i]

def get_classement(pred):
    for i in pred.argsort()[0][::-1]:
        print("#"+str(get_label(i)),":",str(round(pred[0][i]*100,2))+"%")