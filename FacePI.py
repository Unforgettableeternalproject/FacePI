#!/usr/bin/env python

import sys, os, json, time, fire
import ClassUtils as Utils

basepath = os.path.dirname(os.path.realpath(__file__))
config = Utils.loadConfig()
personGroupId = config['personGroupId']
api_key = config['api_key']
host = config['host']


class FacePI:
    
    def Config(self):

        '''Json Settings.'''

        api_key = input('Enter API Key:[' + config['api_key'] + ']:')
        if api_key != '':
            config['api_key'] = api_key
        host = input("Identifying Host...[" + config['host'] + "]: ")
        if host != '':
            config['host'] = host
        title = input("Enter title:[" + config['title'] + "]：")
        if title != '':
            config['title'] = title
        personGroupId = input(
            "Default personGroupId:[" + config['personGroupId'] + "]：")
        if personGroupId != '':
            config['personGroupId'] = personGroupId
        confidence = input("Default confidence:[" + str(config['confidence']) + "]：")
        if confidence != '':
            config['confidence'] = float(confidence)
        landmark = input("Default face landmark set value:[" + str(config['landmark']) + "]：")
        if landmark != '':
            config['landmark'] = int(landmark)
        videoid = input("Camara Id:[" + str(config['videoid']) + "]：")
        if videoid != '':
            config['videoid'] = int(videoid)

        with open(basepath + '/Config.json', 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, ensure_ascii=False)

    def setAPIKEY(self, api_key):
        ''' API fast settings. '''
        config['api_key'] = api_key
        with open(basepath + '/Config.json', 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, ensure_ascii=False)

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
                print("[Error {0}]Connection Failed {1}", format(e.errno, estrerror))
