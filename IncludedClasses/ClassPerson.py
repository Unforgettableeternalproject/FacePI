import http.client, urllib.request, urllib.parse, urllib.error, json
import IncludedClasses.ClassConfig
import IncludedClasses.ClassPersonGroup

config = IncludedClasses.ClassConfig.Config().readConfig()

class Person:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def add_a_person_face(self, imagepath, personId, personGroupId):
        print(
            "'add_a_person_face': put a person ID for a new registered person [personID = " + personId + " ]",
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

    def create_a_person(self, personGroupId, name, userData):
        print(
            "'create_a_person': creating a person [person_name = "
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

        if "error" in create_a_person_json:
            print("Error: " + create_a_person_json["error"]["code"])
            if create_a_person_json["error"]["code"] == "PersonGroupNotFound":
                personGroupApi = IncludedClasses.ClassPersonGroup.PersonGroup()
                personGroupApi.createPersonGroup(
                    config["personGroupID"], config["personGroupName"], "group userdata"
                )
                return self.create_a_person(personGroupId, name, userData)
        return create_a_person_json["personId"]

    def add_personimages(self, personGroupId, personname, userData,
                           imagepaths):
        print("personname=", personname, "imagepath:", imagepaths)
        # person = self.getPersonByName(personGroupId, personname)
        # if person == None:
        print("call create_a_person")
        personid = self.create_a_person(personGroupId, personname, userData)
        for imagepath in imagepaths:
            self.add_a_person_face(imagepath, personid, personGroupId)

    def get_a_person(self, personId, personGroupId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons/" + personId + "?%s" % params, "{body}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            personjson = json.loads(str(data, 'UTF-8'))
            conn.close()
            return personjson
            
        except Exception as e:
            print("[Errno {0}]Disconnected. Please Check you Internet Connection. {1}".format(e.errno, e.strerror))
