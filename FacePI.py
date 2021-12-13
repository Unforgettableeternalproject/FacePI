#!/usr/bin/env python

import sys, os, json, time, fire
import http.client, urllib.request, urllib.parse, urllib.error, base64

basepath = os.path.dirname(os.path.realpath(__file__))
configpath = os.path.join(basepath, 'Config.json')

class FacePI:
    
    def writeConfig(self, config):
        with open(configpath, 'w', encoding='utf-8') as f:
            json.dump(config, f)

    def readConfig(self):
        if not os.path.exists(configpath):
            config = dict()
            config['api_key'] = "b9160fbd882f47bd821205a4bce64354"
            config['host'] = "eastasia.api.cognitive.microsoft.com"
            config['confidence'] = 0.6
            config['title'] = '測試API程式'
            config['personGroupName'] = '人群名稱'
            config['personGroupID'] = 'default_personGroupID'
            self.writeConfig(config)

        with open(configpath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    def detectLocalImage(self, imagepath):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.readConfig()['api_key'],
        }

        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age, gender',

            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
            'faceIdTimeToLive': '86400',
        })

        print('imagepath=', imagepath)
        requestbody = open(imagepath, "rb").read()

        try:
            conn = http.client.HTTPSConnection(self.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params. requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, 'UTF-8'))
            print("detectLocalImage.faces=", json_face_detect)

            conn.close()

            print("detectLocalImage:", f"{imagepath} detected {len(json_face_detect)} people.")

            return json_face_detect
        except Exception as e:
            print("[Errno {0}]Connection Failed {1}".format(e.errno, e.strerror))

    def detectImageUrl(self, imageurl):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apie-Subscription-Key': self.readConfig()['api_key'],
        }

        params = urllib.parse.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age, gender',

            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
            'faceIdTimeToLive': '86400',
        })

        print('imageurl=', imageurl)
        requestbody = '{"url": "' + imageurl + '"}'
        try:
            conn = http.client.HTTPSConnection(self.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody, headers)

            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, 'UTF-8'))
            print("detectImageUrl.faces=", json_face_detect)
            conn.close()

            return json_face_detect

        except Exception as e:
            print("[Errno {0}]Connection Failed {1}".format(e.errno, e.strerror))

        def Signin(self):
            imageurl = 'https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTE4MDAzNDEwNzg5ODI4MTEw/barack-obama-12782369-1-402.jpg'
            self.detectImageUrl(imageurl)

if __name__ == '__main__':
    fire.Fire(FacePI)
