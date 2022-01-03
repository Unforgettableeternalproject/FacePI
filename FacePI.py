#!/usr/bin/env python

import sys, os, json, time, fire
import cv2
from cv2 import waitKey
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
        self.config = IncludedClasses.ClassConfig.Config()

    def Train(self, userData = None, personname = None):
        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = IncludedClasses.ClassOpenCV.show_opencv(hint=" (Picture No. " + str(i + 1) + " )")
            jpgimagepaths.append(jpgimagepath)

        if personname == None:
            personname = input("Enter your name: ")

        if userData == None:
            userData = input("Enter description for yourself (Ex: My Name Is Bernie.): ")

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

        

        personAPI = IncludedClasses.ClassPerson.Person()
        personAPI.add_personimages(self.config.readConfig()['personGroupID'], personname, userData, jpgtrainpaths)
        personGroupapi = IncludedClasses.ClassPersonGroup.PersonGroup()
        personGroupapi.train_personGroup(self.config.readConfig()['personGroupID'])

    def Identify(self, pictureurl):
        start = int(round(time.time() * 1000))
        print("Start estimating [\"identify\"]")
        faceApi = IncludedClasses.ClassFacePI.Face()
        personApi = IncludedClasses.ClassPerson.Person()
        print("Loading IncludedClass", int(round(time.time() * 1000) - start), "ms")

        if pictureurl.startswith("http"):
            detectfaces = faceApi.detectImageUrl(pictureurl)
        else:
            pictureurl = pictureurl.strip()
            
            detectfaces = faceApi.detectLocalImage(pictureurl)


        faceids = []
        for detectface in detectfaces:
            print("Identified FaceId = ", detectface["faceId"])
            faceids.append(detectface["faceId"])

        print("Identify.detectfaces=", detectfaces)

        identifiedfaces = faceApi.identify(faceids[:10], self.config.readConfig()["personGroupID"])
        print("Detected provided [\"identifyfaces\"] with amount of ", len(identifiedfaces))

        # successes = []
        for identifiedface in identifiedfaces:
            for candidate in identifiedface["candidates"]:
                personId = candidate["personID"]
                person = personApi.get_a_person(personId, self.config.readConfig()["personGroupID"])
                identifiedface["person"] = person
                identifiedface["confidence"] = candidate["confidence"]
                identifiedface["personID"] = candidate["personID"]

        for identifyface in identifiedfaces:
            if "person" not in identifyface:
                print("identifyface=", identifyface)
                print("Can't identify the person, please do training first.")
            else:
                name = identifyface["person"]["name"]
                confidence = float(identifyface["confidence"])
                if confidence >= 0.9:
                    print(name + "Signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with SUCCULENT result.")
                elif confidence >= 0.8:
                    print(name + "Signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with Great result.")
                elif confidence >= 0.7:
                    print(name + "Signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with good result.")
                else:
                    print(name + "Signed in successfully." + f"[With a Confidence of {confidence}]")


    def Signin(self):
        imagepath = IncludedClasses.ClassOpenCV.show_opencv()
        # json_face_detect = classes.ClassFaceAPI.Face().detectLocalImage(imagepath)
        self.Identify(imagepath)


pi = FacePI()

commandString = "\nAcceptible Commands:\n Sign in: 'sign_in',\n Train: 'train',\n End Program: 'end'."

#Master
print("Awiting command...\n" + commandString)
answer = ''
while(answer != 'end'):
    answer = input()
    if(answer == 'sign_in'):
        pi.Signin()
    elif(answer == 'traing'):
        pi.Train()
    elif(answer == 'end'):
        pass
    else:
        print('Invaild command!\n' + commandString + '\n')

print('Program Ended.')

cv2.waitKey(0)

#if __name__ == '__main__':
#    fire.Fire(FacePI)
