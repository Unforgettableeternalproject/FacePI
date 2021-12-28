import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import IncludedClasses.ClassConfig
config = IncludedClasses.ClassConfig.Config().readConfig()

class Person:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def add_a_person_face(self, imagepath, personId, personGroupId):
        print(
            "'add_a_person_face': put a person ID for a new registered person[personId = " + personId + " ]",
            "imagepath=",
            imagepath,
        )

        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        params = urllib.parse.urlencode(
            {
                # Request parameters
                "personGroupId": personGroupId,
                #'personId': '03cb1134-ad35-4b80-8bf2-3200f44eef31',
                "personId": personId,
                #'userData': '{string}',
                #'targetFace': '{string}',
            }
        )
        requestbody = open(imagepath, "rb").read()

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/"
                + personGroupId
                + "/persons/"
                + personId
                + "/persistedFaces?%s" % params,
                requestbody,
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            jsondata = json.loads(str(data, "UTF-8"))
            conn.close()

        except Exception as e:
            print("[Errno {0}]Disconnected. Please Check you Internet Connection. {1}".format(e.errno, e.strerror))

        try:
            if ClassUtils.isFaceAPIError(jsondata):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.add_a_person_face(imagepath, personId, personGroupId)
        except MyException.UnspecifiedError as e:
            return

    def create_a_person(self, personGroupId, name, userData):
        print(
            "'create_a_person': creating a person [person name = "
            + name
            + " ] inside a person group [personGroupID = "
            + personGroupId
            + " ]"
        )
        headers = {
            # Request headers
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        params = urllib.parse.urlencode({"personGroupId": personGroupId})
        requestbody = '{"name":"' + name + '","userData":"' + userData + '"}'

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params,
                requestbody.encode("UTF-8"),
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            create_a_person_json = json.loads(str(data, "UTF-8"))
            conn.close()
        except Exception as e:
            print("[Errno {0}]Disconnected. Please Check you Internet Connection. {1}".format(e.errno, e.strerror))

        try:
            if ClassUtils.isFaceAPIError(create_a_person_json):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.create_a_person(personGroupId, name, userData)
        except MyException.PersonGroupNotFoundError as e:
            personGroupApi = PersonGroup(self.api_key, self.host)
            personGroupApi.createPersonGroup(
                config["personGroupId"], config["personGroupName"], "group userdata"
            )
            return self.create_a_person(personGroupId, name, userData)
        except MyException.UnspecifiedError as e:
            return

        return create_a_person_json["personId"]

    def add_personimages(self, personGroupId, personname, userData,
                           imagepaths):
        print("personname=", personname, "image path:", imagepaths)
        person = self.getPersonByName(personGroupId, personname)
        if person == None:
            print('call create_a_person')
            personid = self.create_a_person(personGroupId, personname,
                                                 userData)
            for imagepath in imagepaths:
                self.add_a_person_face(imagepath, personid, personGroupId)
        else:
            print('call add_a_person_face, personId=', person['personId'])
            for imagepath in imagepaths:
                self.add_a_person_face(imagepath, person['personId'],
                                            personGroupId)