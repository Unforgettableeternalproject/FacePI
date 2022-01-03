#!/usr/bin/env python

import sys, os, json, time, fire
import cv2
from cv2 import waitKey
import http.client, urllib.request, urllib.parse, urllib.error, base64
import IncludedClasses.ClassFacePI
import IncludedClasses.ClassOpenCV
import IncludedClasses.ClassPerson
import IncludedClasses.ClassPersonGroup
import IncludedClasses.ClassConfig

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
            userData = input("Enter description for yourself (Ex: My Name Is Bernie): ")

        jpgtrainpaths = []
        for jpgimagepath in jpgimagepaths:
            basepath = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.basename(jpgimagepath)
            jpgtrainpath = os.path.join(
                basepath, "traindatas", userData, personname, filename
            )
            if not os.path.exists(os.path.dirname(jpgtrainpath)):
                os.makedirs(os.path.dirname(jpgtrainpath))
            os.rename(jpgimagepath, jpgtrainpath)
            jpgtrainpaths.append(jpgtrainpath)

        

        personAPI = IncludedClasses.ClassPerson.Person()
        personAPI.add_personimages(self.config.readConfig()['personGroupID'], personname, userData, jpgtrainpaths)
        personGroupapi = IncludedClasses.ClassPersonGroup.PersonGroup()
        personGroupapi.train_personGroup()

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
        print("Detected provided [\"identifyfaces\"] with amount of", len(identifiedfaces))

        print(identifiedfaces)
        # successes = []
        for identifiedface in identifiedfaces:
            for candidate in identifiedface["candidates"]:
                personId = candidate["personId"]
                person = personApi.get_a_person(personId, self.config.readConfig()["personGroupID"])
                identifiedface["person"] = person
                identifiedface["confidence"] = candidate["confidence"]
                identifiedface["personID"] = candidate["personId"]

        for identifyface in identifiedfaces:
            if "person" not in identifyface:
                print("identifyface=", identifyface)
                print("Can't identify the faces, please do training first.")
            else:
                name = identifyface["person"]["name"]
                confidence = float(identifyface["confidence"])
                if confidence >= 0.9:
                    print(name + " signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with SUCCULENT result.")
                elif confidence >= 0.8:
                    print(name + " signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with Great result.")
                elif confidence >= 0.7:
                    print(name + " signed in successfully." + f"[With a Confidence of {confidence}]\n" + "estimation ended with good result.")
                else:
                    print(name + " signed in successfully." + f"[With a Confidence of {confidence}]")

    def Debug(self):
        
        print("Debug Mode Activated, awaiting command...\n")
        answer = ''
        while(answer != 'leave'):
            print("Awiting command...\n" + commandString[1])
            answer = input()
            if(answer == 'f_dt'):
                print('\n')
                imagepath = IncludedClasses.ClassOpenCV.show_opencv()
                self.detect.detectLocalImage(imagepath)
                print('Returning to debug console...')
            elif(answer == 'f_id_local'):
                print('\n Require image path: ')
                imagepath = input()
                pi.Signin(imagepath)
                print('Returning to debug console...')
            elif(answer == 'f_id_url'):
                print('\n Require image url: ')
                imageurl = input()
                pi.Signin(imageurl)
                print('Returning to debug console...')
            elif(answer == 'p_json'):
                print('\n')
                print("Printing Json File (config.json):\n")
                print(f"{self.config.readConfig()['api_key']}\n{self.config.readConfig()['host']}\n{self.config.readConfig()['confidence']}\n{self.config.readConfig()['title']}\n{self.config.readConfig()['personGroupName']}\n{self.config.readConfig()['personGroupID']}")
            elif(answer == 'leave'):
                pass
            else:
                print('Invaild command!\n')
    
        print('Leaving Debug Mode...\n')

    def Signin(self, ip):
        if(ip != ''):
            imagepath = ip
        else:
            imagepath = IncludedClasses.ClassOpenCV.show_opencv()
        # json_face_detect = classes.ClassFaceAPI.Face().detectLocalImage(imagepath)
        self.Identify(imagepath)


pi = FacePI()

commandString = ["\nAcceptible Commands:\n Sign in: 'sign_in',\n Train: 'train',\n Enter Debug Mode: 'debug',\n End Program: 'end'.", 
                "\nAcceptible Commands:\n Face Detection(Only scan charateristics): 'f_dt',\n Face Identification(Local Image): 'f_id_local',\n Face Identification(From Internet): 'f_id_url',\n Print Config.json: 'p_json',\n Leave Debug Mode: 'leave'."]

#Master
answer = ''
while(answer != 'end'):
    print("Awiting command...\n" + commandString[0])
    answer = input()
    if(answer == 'sign_in'):
        print('\n')
        pi.Signin('')
        print('Returning to master console...')
    elif(answer == 'train'):
        print('\n')
        pi.Train()
        print('Returning to master console...')
    elif(answer == 'debug'):
        print('\n')
        pi.Debug()
    elif(answer == 'end'):
        pass
    else:
        print('Invaild command!\n')
    
print('Program Ended.')

cv2.waitKey(0)

#if __name__ == '__main__':
#    fire.Fire(FacePI)