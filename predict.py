from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import numpy as np
from constants import img_height, img_width, channel_width
from classes import class_names
from sys import argv
from io import BytesIO
import requests
from PIL import Image

Model = load_model("./models/model.h5")
target_size = (img_width, img_height, channel_width)


def loadImage(url):
    """Load the image from the Telegram's server and save it in a variable"""
    response = requests.get(url)
    img_bytes = BytesIO(response.content)
    img = Image.open(img_bytes)
    img = img.convert('RGB')
    img = img.resize((img_width, img_height), Image.NEAREST)
    img = img_to_array(img)
    return img


def predict_model(url):
    """Predict the model based Images send as an Input 128 widthx128 height"""
    img_array = []
    if url.startswith("http"):
        img_array = loadImage(url)
    else:
        img = load_img(url, target_size=target_size)
        img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    result = Model.predict(img_array)
    itemindex = np.where(result == np.max(result))
    plant_name,disease_name=map(lambda x: x.replace("_"," "),class_names[itemindex[1][0]].split("___"))
    return "Name of the plane: "+plant_name+"\n Disease: "+disease_name
