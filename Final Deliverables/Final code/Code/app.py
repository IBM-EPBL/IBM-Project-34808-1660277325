from flask import Flask,render_template,request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests

app = Flask(_name_,template_folder="templates")
model=load_model('nutrition.h5')
print("Loaded model from disk")

@app.route('/')
def home():
    return render_template('home.hmtl')

@app.route('/image',method=['GET','POST'])
def image1():
    return render_template("image.html")

@app.route('/predict',methods=['GET','POST'])
def launch():
    if request.method=='POST':
        f=request.files['file']
        basepath=os.path.dirname('_file_')
        filepath=os.path.join(basepath,"uploads",f.filename)
        f.save(filepath)

        img=image.load_img(filepath,target_size=(64,64))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)

        pred=np.argmax(model.predic(x),axis=1)
        print("prediction",pred)
        index=['APPLES','BANANA','ORANGE','PINEAPPLE','WATERMELON']

        result=str(index[pred[0]])

        x=result
        print(x)
        result=nutrition(result)
        print(result)

        return render_template("0.html",showcase=(result),showcase1=(x))

        def nutrition(index):

            url="https://calorieninjas.p.rapidapi.com/v1/nutrition"

            querystring = {"query":index}

            headers= {
                'x-rapidapi-key': "5d797ab107mshe668f26bd044e64p1ffd34jsnf47bfa9a8ee4",
                'x-rapidapi-host': "calorieninjas.p.rapidapi.com"
            }
        response= requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        return response.json()['items']

