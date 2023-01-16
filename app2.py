import cv2
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask,flash, render_template, request, redirect, url_for ,jsonify
import fun as functions
import os
from werkzeug.utils import secure_filename
import json

choicemag2 =0
choicemag1 =0



app = Flask(__name__)

UPLOAD_FOLDER = './static/uploader'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload/<int:image_id>',methods=['POST'])
def upload_file(image_id):
    global filepath1,filepath2,mag1,pha1,mag2,pha2
    if image_id==1:
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath1=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath1)
            mag1,pha1=functions.image.get_components(filepath1,1)
            
    elif image_id==2:
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath2=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath2)
            mag2,pha2=functions.image.get_components(filepath2,2)
            select=1
            functions.Processing.mixer(mag1,pha1,mag2,pha2,select)
    elif image_id==3:
        select=2
        functions.Processing.mixer(mag1,pha1,mag2,pha2,select)

    elif image_id==6:
        select=1
        functions.Processing.mixer(mag1,pha1,mag2,pha2,select)

    elif image_id==4:
        mag11,pha22=functions.Processing.requested_data(mag1,pha2)
        select=1
        functions.Processing.mixer(mag11,pha1,mag2,pha22,select)

    elif image_id==5:
        mag22,pha11=functions.Processing.requested_data(mag2,pha1)
        select=2
        functions.Processing.mixer(mag1,pha11,mag22,pha2,select)
    


    return jsonify("0")



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True,port=9040)

