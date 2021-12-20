#!/usr/bin/env python

import sys, os, json, time, fire
import http.client, urllib.request, urllib.parse, urllib.error, base64
import IncludedClasses.ClassFacePI

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

class FacePI:
    
    def __init__(self):
        self.detect = IncludedClasses.ClassFacePI.Face()

    def Signin(self):
        imageurl = 'https://upload.wikimedia.org/wikipedia/commons/1/18/Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg'
#        imagepath = r'C:/Users/user/Desktop/Bernie/FacePI/SomeGuyOnTheInternet.jpg'

        self.detect.detectImageUrl(imageurl)
#        self.detect.detectLocalImage(imagepath)

pi = FacePI()

pi.Signin()

#if __name__ == '__main__':
#    fire.Fire(FacePI)
