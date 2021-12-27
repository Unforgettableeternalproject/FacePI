#!/usr/bin/env python

import sys, os, json, time, fire
import http.client, urllib.request, urllib.parse, urllib.error, base64
import IncludedClasses.ClassFacePI
import IncludedClasses.ClassOpenCV

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

def show_opencv():
        IncludedClasses.ClassOpenCV.show_opencv(' Smile :)')

class FacePI:
    
    def __init__(self):
        self.detect = IncludedClasses.ClassFacePI.Face()

    def Signin(self):
#        imageurl = 'https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.15752-9/266785464_1258584021314938_5117372255658393059_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=ae9488&_nc_ohc=FRyIgWcoFM0AX_e2Pb-&_nc_ht=scontent.fkhh1-1.fna&oh=03_AVIHgJdbHOCJUzkVG7U_rQIykLTYZ7gIwD7TlFyAunT3ig&oe=61E808E9'
        imagepath = r'C:/Users/user/Desktop/Bernie/FacePI/LocalImages/AfterImage.jpg'

#        self.detect.detectImageUrl(imageurl)
        self.detect.detectLocalImage(imagepath)

# show_opencv()
pi = FacePI()

pi.Signin()

#if __name__ == '__main__':
#    fire.Fire(FacePI)
