import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import IncludedClasses.ClassConfig
config = IncludedClasses.ClassConfig.Config().readConfig()


class PersonGroup:
    def __init__(self):
        self.api_key = config["api_key"]
        self.host = config["host"]

    def train_personGroup(self):
        personGroupId=config["personGroupID"]
        print(
            "train_personGroup: Starting training for a new personGroup [personGroupId = " + personGroupId + " ]."
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
            print("[Errno {0}]Disconnected. Please Check you Internet Connection. {1}".format(e.errno, e.strerror))