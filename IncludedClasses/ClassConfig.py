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
            config['confidence'] = 0.5
            config['title'] = 'Test API Program'
            config['personGroupName'] = 'GroupName'
            config['personGroupID'] = 'default_personGroupID'
            self.writeConfig(config)

        with open(self.configpath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def setConfig(self):
        config = self.readConfig()
        api_key = input(f'Enter a working API Key:[{config["api_key"]}]: ')
        if api_key: config['api_key'] = api_key
        title = input(f'Enter title:[{config["title"]}]: ')
        if title: config['title'] = title

        self.writeConfig(config)