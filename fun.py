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
        img1=cv2.resize(img1,(270,230
        
        
        ))
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

    def mask(img,x,y,w,h):
        mask0=img
        mask1=np.zeros(mask0.shape,np.uint8)
        mask1[int(y):int(y)+int(h),int(x):int(x)+int(w)]=mask0[int(y):int(y)+int(h),int(x):int(x)+int(w)]
        return mask1
    

    def requested_data(img1,img2):
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

        masking1=Processing.mask(img1,x1,y1,w1,h1)

        masking2=Processing.mask(img2,x2,y2,w2,h2)
        print(data)

        return masking1,masking2


    def mixer(magnitude,phase,magnitude2,phase2,select):
        if select ==1:
            print("mag of first and phase of second")
            img_comb = np.multiply(magnitude, np.exp(1j * phase2))
            resulting_img= np.real(np.fft.ifft2(np.fft.ifftshift(img_comb)))
        if select==2:
            print("mag of second and phase of first")
            img_comb = np.multiply(magnitude2, np.exp(1j * phase))
            resulting_img= np.real(np.fft.ifft2(img_comb))

        # resulting_img=np.abs(resulting_img)
    
        saved_path='./static/images/combined.jpg'
        plt.imsave(saved_path,np.abs(resulting_img), cmap='gray')    
        return saved_path


    
    # def main(path1,index):
    #     img1_path  =0
    #     img2_path =0

    #     if index ==1:
    #         img1_path==path1
    #     else:
    #         img2_path=path1 

    #     default_path='./static/images/Pulse-Sensor-Pinout.png'
    #     img_default=image.read(default_path)
    #     img_default=image.resize(img_default)
    #     mag_default=image.get_magnitude(img_default)
    #     phase_defualt=image.get_phase(img_default)
        
    #     if index==1:
    #         mag1,phase1=image.get_components(img1_path,1)
    #         # mag1=Processing.check(mag1,x,y,h,w)
    #         # phase1=Processing.check(phase1,x,y,h,w)
    #     else:
    #         mag2,phase2=image.get_components(img2_path,2)
    #         # mag2=Processing.check(mag1,x,y,h,w)
    #         # phase2=Processing.check(phase2,x,y,h,w)
    
    #     if (img1_path == None and img2_path != None):
    #         Image.mixer(mag_default,phase_defualt,mag2,phase2,select)
        
    #     elif (img1_path !=None and img2_path ==None):
    #         Image.mixer(mag1,phase1,mag_default,phase_defualt,select)
    #     else  :
    #         Image.mixer(mag1,phase1,mag2,phase2,select)