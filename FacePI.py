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
#        imageurl = 'https://upload.wikimedia.org/wikipedia/commons/1/18/Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg'
        imagepath = r'D:/Materials/Programs/Python/FacePI/LocalImages/YouSuck.jpg'

#        self.detect.detectImageUrl(imageurl)
        self.detect.detectLocalImage(imagepath)

# show_opencv()
pi = FacePI()

pi.Signin()

#if __name__ == '__main__':
#    fire.Fire(FacePI)
