#!/usr/bin/env python

import sys, os, json, time, fire
import http.client, urllib.request, urllib.parse, urllib.error, base64
import IncludedClasses.ClassFacePI
import IncludedClasses.ClassOpenCV
import IncludedClasses.ClassPerson
import IncludedClasses.ClassPersonGroup

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

def show_opencv():
        return IncludedClasses.ClassOpenCV.show_opencv(' Smile :)')

class FacePI:
    
    def __init__(self):
        self.detect = IncludedClasses.ClassFacePI.Face()

    def Train(self, userData = None, personname = None):
        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = IncludedClasses.ClassOpenCV.show_opencv(hint=" (Picture No. " + str(i + 1) + " )")
            jpgimagepaths.append(jpgimagepath)

        if personname == None:
            personname = input("Enter your name: ")

        if userData == None:
            userData = input("Enter description for yourself (Ex: My Name Is Bernie): ")

        jpgtrainpaths = []
        for jpgimagepath in jpgimagepaths:
            filename = os.path.basename(jpgimagepath)
            home = os.path.expanduser("~")
            jpgtrainpath = os.path.join(
                home, "traindatas", userData, personname, filename
            )
            if not os.path.exists(os.path.dirname(jpgtrainpath)):
                os.makedirs(os.path.dirname(jpgtrainpath))
            os.rename(jpgimagepath, jpgtrainpath)
            jpgtrainpaths.append(jpgtrainpath)


        myconfig = IncludedClasses.ClassConfig.Config()
        

        personAPI = IncludedClasses.ClassPerson.Person()
        personAPI.add_personimages(myconfig['personGroupID'], personname, userData, jpgtrainpaths)
        personGroupapi = IncludedClasses.ClassPersonGroup.PersonGroup()
        personGroupapi.train_personGroup(myconfig['personGroupID'])

    def Signin(self):
#        imageurl = 'https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.15752-9/266785464_1258584021314938_5117372255658393059_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=ae9488&_nc_ohc=FRyIgWcoFM0AX_e2Pb-&_nc_ht=scontent.fkhh1-1.fna&oh=03_AVIHgJdbHOCJUzkVG7U_rQIykLTYZ7gIwD7TlFyAunT3ig&oe=61E808E9'
#        imagepath = r'C:/Users/user/Documents/FacePI/FacePI/LocalImages/AfterImage.jpg'

#        self.detect.detectImageUrl(imageurl)
        imagepath = IncludedClasses.ClassOpenCV.show_opencv()
        #json_face_detect = 
        self.detect.detectLocalImage(imagepath)

pi = FacePI()

pi.Signin()

#if __name__ == '__main__':
#    fire.Fire(FacePI)
