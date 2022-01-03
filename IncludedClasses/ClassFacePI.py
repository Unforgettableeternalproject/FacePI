import http.client, urllib.request, urllib.parse, urllib.error, json
import urllib, http, json, time, sys
import IncludedClasses.ClassConfig

class Face:
    def __init__(self):
        self.config = IncludedClasses.ClassConfig.Config()

    def detectLocalImage(self, imagepath):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.config.readConfig()['api_key'],
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
            conn = http.client.HTTPSConnection(self.config.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody, headers)
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
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.config.readConfig()['api_key'],
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender',
            #'recognitionModel': 'recognition_04',
            'returnRecognitionModel': 'false',
            'detectionModel': 'detection_01',
            'faceIdTimeToLive': '86400',
        })
        #'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure'
        print('imageurl=', imageurl)
        requestbody = '{"url": "' + imageurl + '"}'
        try:
            conn = http.client.HTTPSConnection(self.config.readConfig()['host'])
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                         headers)
            response = conn.getresponse()
            data = response.read()
            json_face_detect = json.loads(str(data, 'UTF-8'))
            print("detectLocalImage.faces=", json_face_detect)
            conn.close()

            print("detectImageUrl:",
                f"{imageurl} detected {len(json_face_detect)} people(person)")
            return json_face_detect
            
        except Exception as e:
            print("[Errno {0}]Connection Failed {1}".format(e.errno, e.strerror))

    def identify(self, faceidkeys, personGroupId):
        print("def Face.identify start identifying。faceidkeys=", faceidkeys)
        if len(faceidkeys) == 0:
            return []
        start = int(round(time.time() * 1000))
        print("Start identify 0 ms")

        headers = {
            # Request headers
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.config["api_key"],
        }

        params = urllib.parse.urlencode({})

        requestbody = (
            '''{
            "personGroupId": "'''
            + personGroupId
            + """",
            "faceIds":"""
            + str(faceidkeys)
            + """,
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": """
            + str(self.config["confidence"])
            + """
        }"""
        )
        # print('requestbody=', requestbody)
        try:
            conn = http.client.HTTPSConnection(self.config['host'])
            conn.request(
                "POST", "/face/v1.0/identify?%s" % params, requestbody, headers
            )
            response = conn.getresponse()
            data = response.read()
            identifiedfaces = json.loads(str(data, "UTF-8"))
            print("Face.Identify.identifiedfaces=", identifiedfaces)
            conn.close()
            # ClassUtils.tryFaceAPIError(identifyfaces)
        except Exception as e:
            print("[Errno {0}]Disconnected. Please Check you Internet Connection. {1}".format(e.errno, e.strerror))
            sys.exit()

        if "error" in identifiedfaces:
            print("Error: " + identifiedfaces["error"]["code"])
            if identifiedfaces['error']['code'] == 'PersonGroupNotFound':
                personGroupAPI = IncludedClasses.ClassPersonGroup.PersonGroup()
                personGroupAPI.createPersonGroup(
                    personGroupId, self.config["personGroupName"], "group userdata"
                )
                return self.identify(faceidkeys, personGroupId)
        return identifiedfaces