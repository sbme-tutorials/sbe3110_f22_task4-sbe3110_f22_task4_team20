import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect
import cv2
# from skimage import io
import matplotlib.pylab as plt


select=0

class image:
    def read(path):
        img1=cv2.imread(path,0)
        return img1
    
    def resize(img1):
        img1=cv2.resize(img1,(270,230))
        return img1
    
    def fourier(img1):
        img1_fft = np.fft.fftshift(np.fft.fft2(img1))
        return img1_fft
    
    def get_magnitude(img1_fft):
        img1_amplitude = np.sqrt(np.real(img1_fft) ** 2 + np.imag(img1_fft) ** 2)
        return img1_amplitude
    
    def get_phase(img1_fft):
        img1_phase = np.arctan2(np.imag(img1_fft), np.real(img1_fft))
        return img1_phase
    
    def get_components(path,index):
        img1=image.read(path)
        img1=image.resize(img1)
        img1_fft=image.fourier(img1)
        mag=image.get_magnitude(img1_fft)
        phase=image.get_phase(img1_fft)

        if index==1:
            saved_mag='./static/images/signal.jpg'
            saved_phase='./static/images/signalphase1.jpg'
        
        elif index==2:
            saved_mag='./static/images/signal2.jpg'
            saved_phase='./static/images/signalphase2.jpg'
        
        
        plt.imsave(saved_mag,np.log(mag+1e-10), cmap='gray')
        plt.imsave(saved_phase,phase, cmap='gray')

        return mag,phase     

class Processing:

    def rectangle(img, x1,y1,w, h, filter_flag):
        image0=img
        x2=x1+w
        y2=y1+h
        x1_axis=int(x1)
        x2_axis=int(x2)
        zero_2d_low = np.zeros_like(image0)
        zero_2d_high= np.zeros_like(image0)
        max_height = image0.shape[0] - 1
        for x in range(x1_axis, x2_axis):
            for y in range(int(y1), int(y2)):
                zero_2d_low[max_height - y, x] = image0[max_height - y, x]
                image0[max_height - y, x] = zero_2d_high[max_height - y, x]
        if filter_flag==0:
            return zero_2d_low
        else:
            return image0
    

    def requested_data(img1,img2,filter_id):
        data=request.get_json()
        #dimensions of rect1 (mag1,mag2)
        x1=data["x1"]
        y1=data["y1"]
        w1=data["w1"]
        h1=data["h1"]
        #dimensions of rect2 (pha1,pha2)
        x2=data["x2"]
        y2=data["y2"]
        w2=data["w2"]
        h2=data["h2"]

        masking1=Processing.rectangle(img1,x1,y1,w1,h1,filter_id)

        masking2=Processing.rectangle(img2,x2,y2,w2,h2,filter_id)
        print(data)

        return masking1,masking2



    def mixer (magnitude,phase):

        img_comb = np.multiply(magnitude, np.exp(1j * phase))
        resulting_img= np.real(np.fft.ifft2(img_comb))
    
        saved_path='./static/images/combined.jpg'
        plt.imsave(saved_path,np.abs(resulting_img), cmap='gray')    
        return saved_path


    