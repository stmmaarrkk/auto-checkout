from selenium import webdriver
import os
import json
import random

class Bootstrap:
    def __init__(self):
        self.configs = {}
        self.prepareConfigs()

    def prepareConfigs(self, configFile="./configs/browser_configs.json"):
        #prepare configs
        assert os.path.isfile(configFile), "browser_configs.json file doesn't exist!"
        with open(configFile, 'r') as f:
            self.configs = json.load(f)

        self.configs["user_agent"] = self.generateUserAgent() #generate fake user-agent
        self.syncBrowserVersion()

    def generateUserAgent(self):
        ua = None
        with open("./configs/user_agent_pool", "r") as f:
            lines = f.readlines()
            randNum = random.randint(0, len(lines)-1)
            ua = lines[randNum]
        assert len(ua) != 0, "user-agent should not be empty"
        return ua

    def launchBrowser(self):
        # inject configs
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('User-Agent="{}"'.format(self.configs["user_agent"]))

        #launch browser
        return webdriver.Chrome(executable_path=self.configs["chrome_driver_path"], options=chromeOptions)

    def syncBrowserVersion(self):
        # substitute dirver version in user agent
        idx1 = self.configs["user_agent"].find("Chrome/") + 7
        idx2 = self.configs["user_agent"][idx1:].find(" ") + idx1
        oldVersion = self.configs["user_agent"][idx1:idx2]
        self.configs["user_agent"] = self.configs["user_agent"].replace(oldVersion, self.configs["chrome_driver_version"])
