#!/usr/bin/env python

import os, time
import urllib.parse, urllib.error
import IncludedClasses.ClassFacePI as PI
import IncludedClasses.ClassOpenCV as CV
import IncludedClasses.ClassPerson as Person
import IncludedClasses.ClassPersonGroup as PG
import IncludedClasses.ClassConfig as Config

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

def show_opencv():
        return CV.show_opencv(' Smile :)')

class FacePI:
    
    def __init__(self):
        self.detect = PI.Face()
        self.config = Config.Config()
        self.result = ''

    def Train(self, userData = None, personname = None):
        self.result = ''
        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = CV.show_opencv(hint=" (Picture No. " + str(i + 1) + " )")
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
                basepath, "../traindatas", userData, personname, filename
            )
            if not os.path.exists(os.path.dirname(jpgtrainpath)):
                os.makedirs(os.path.dirname(jpgtrainpath))
            os.rename(jpgimagepath, jpgtrainpath)
            jpgtrainpaths.append(jpgtrainpath)

        

        personAPI = Person.Person()
        personAPI.add_personimages(self.config.readConfig()['personGroupID'], personname, userData, jpgtrainpaths)
        personGroupapi = PG.PersonGroup()
        personGroupapi.train_personGroup()
        self.result = '>_' + f"{personname} successfully trained!"

    def Identify(self, pictureurl):
        self.result = []
        start = int(round(time.time() * 1000))
        print("Start estimating [\"identify\"]")
        faceApi = PI.Face()
        personApi = Person.Person()
        print("Loading IncludedClass", int(round(time.time() * 1000) - start), "ms")

        if pictureurl.startswith("http"):
            detectfaces = faceApi.detectImageUrl(pictureurl)
        else:
            pictureurl = pictureurl.strip()
            
            detectfaces = faceApi.detectLocalImage(pictureurl)


        faceids = []
        try:
            for detectface in detectfaces:
                print("Identified FaceId = ", detectface["faceId"])
                faceids.append(detectface["faceId"])
        except Exception as e:
            self.result = e
            return
            
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
                self.result.append('>_' + "Can't identify the face, please do training first.")
            else:
                name = identifyface["person"]["name"]
                confidence = float(identifyface["confidence"])
                if confidence >= 0.9:
                    self.result.append('>_' + name + " signed in successfully. " + f"\n>_[With a Confidence of {confidence}]\n" + ">_Estimation ended with SUCCULENT result.")
                elif confidence >= 0.8:
                    self.result.append('>_' + name + " signed in successfully. " + f"\n>_[With a Confidence of {confidence}]\n" + ">_Estimation ended with Great result.")
                elif confidence >= 0.7:
                    self.result.append('>_' + name + " signed in successfully. " + f"\n>_[With a Confidence of {confidence}]\n" + ">_Estimation ended with good result.")
                else:
                    self.result.append('>_' + name + " signed in successfully. " + f"\n>_[With a Confidence of {confidence}]")

    def Signin(self, ip):
        if(ip != ''):
            imagepath = ip
        else:
            imagepath = CV.show_opencv(" Smile :).")
        # json_face_detect = classes.ClassFaceAPI.Face().detectLocalImage(imagepath)
        self.Identify(imagepath)