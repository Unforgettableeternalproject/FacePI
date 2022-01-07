import http.client, urllib.request, urllib.parse, urllib.error, json
import IncludedClasses.ClassConfig
config = IncludedClasses.ClassConfig.Config().readConfig()


class PersonGroup:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def train_personGroup(self):
        personGroupId=config["personGroupID"]
        print(
            "train_personGroup: Starting training for a new personGroup [personGroupID = " + personGroupId + " ]."
        )

        headers = {
            # Request headers
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        params = urllib.parse.urlencode({"personGroupID": personGroupId})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST",
                "/face/v1.0/persongroups/" + personGroupId + "/train?%s" % params,
                "{body}",
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}]Connection Failed. Please check your Internet Connection. {1}".format(e.errno, e.strerror))

    def createPersonGroup(self, personGroupId, groupname, groupdata):
        print("createPersonGroup: Create a personGroup ID [personGroupID = " + personGroupId + " ].")
        headers = {
            # Request headers.
            "Content-Type": "application/json",
            # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
            "Ocp-Apim-Subscription-Key": self.api_key,
        }

        body = "{ 'name':'" + groupname + "', 'userData':'" + groupdata + "' }"

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "PUT",
                "/face/v1.0/persongroups/{}".format(personGroupId),
                body.encode(encoding="utf-8"),
                headers,
            )
            print("=============")
            response = conn.getresponse()
            data = response.read()
            jsondata = json.loads(str(data, "UTF-8"))
            print(jsondata)

            print(response.reason)
            conn.close()
            self.train_personGroup()
            return personGroupId
        except Exception as e:
            print(e.args)