import sys, os, json

class Config:

    def __init__(self):
        basepath = os.path.dirname(os.path.realpath(__file__))
        self.configpath = os.path.join(basepath, 'Config.json') 

    def writeConfig(self, config):
        with open(self.configpath, 'w', encoding='utf-8') as f:
            json.dump(config, f)

    def readConfig(self):
        if not os.path.exists(self.configpath):
            config = dict()
            config['api_key'] = "b9160fbd882f47bd821205a4bce64354"
            config['host'] = "eastasia.api.cognitive.microsoft.com"
            config['confidence'] = 0.6
            config['title'] = '測試API程式'
            config['personGroupName'] = '人群名稱'
            config['personGroupID'] = 'default_personGroupID'
            self.writeConfig(config)

        with open(self.configpath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config