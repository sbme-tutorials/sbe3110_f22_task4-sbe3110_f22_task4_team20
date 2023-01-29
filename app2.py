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
    global filepath1,filepath2,mag1,pha1,mag2,pha2,filter_id
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
            filter_id=0
            functions.Processing.mixer(mag1,pha2)
            
    elif image_id==10:
        filter_id=1


    elif image_id==11:
        filter_id=0


    elif image_id==3:
        functions.Processing.mixer(mag2,pha1)

    elif image_id==6:
        functions.Processing.mixer(mag1,pha2)

    elif image_id==4:
        cropped_magnitude1,copped_phase2=functions.Processing.requested_data(mag1,pha2,filter_id)
        functions.Processing.mixer(cropped_magnitude1,copped_phase2)

    elif image_id==5:
        cropped_magnitude2,copped_phase1=functions.Processing.requested_data(mag2,pha1,filter_id)
        functions.Processing.mixer(cropped_magnitude2,copped_phase1)
    


    return jsonify("0")



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True,port=5007)

