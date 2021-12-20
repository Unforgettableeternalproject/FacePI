#!/usr/bin/env python

import sys, os, json, time, fire
import http.client, urllib.request, urllib.parse, urllib.error, base64
import IncludedClasses.ClassFacePI

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

class FacePI:
    
    def __init__(self) -> None:
        self.detectIU = IncludedClasses.ClassFacePI.Face().detectImageUrl()
        self.detectLI = IncludedClasses.ClassFacePI.Face().detectLocalImage()

    def Signin(self):
        imageurl = 'https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTE4MDAzNDEwNzg5ODI4MTEw/barack-obama-12782369-1-402.jpg'
#        imagepath = r'C:/Users/user/Desktop/Bernie/FacePII/barack-obama-12782369-1-402.jpg'

        self.detectIU(imageurl)
 #       self.detectLI(imagepath)

pi = FacePI()

pi.Signin()

if __name__ == '__main__':
    fire.Fire(FacePI)
