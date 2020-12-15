from bs4 import BeautifulSoup
import requests
from io import BytesIO
from selenium import webdriver
from urllib.request import urlopen
from zipfile import ZipFile
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

        updated = False
        if self.configs["chrome_driver_version"] == "":
            updated = True
            self.downloadChromeDriver()

        #"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",

        self.configs["user_agent"] = self.generateUserAgent() #generate fake user-agent
        self.syncBrowserVersion()

        if updated: #save and reload again
            with open(configFile, 'w') as f:
                json.dump(self.configs, f)

            with open(configFile, 'r') as f:
                self.configs = json.load(f)

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
    def downloadChromeDriver(self):
        """
        will return dirvers full path
        """
        ## find resource
        print("Locating driver URL...")
        homeURL = "https://chromedriver.chromium.org"
        response = requests.get(homeURL)
        soup = BeautifulSoup(response.text, "html.parser")
        version = soup.find('span', text='Latest stable ').parent.find('a', href=True).text
        version = version.replace("ChromeDriver", "").replace(" ", "")
        downloadURL = "https://chromedriver.storage.googleapis.com/{}/chromedriver_mac64.zip".format(version)
        #"https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_mac64.zip"

        #download and unzip
        print("Downloading driver from {}".format(downloadURL))
        with urlopen(downloadURL) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                if os.path.isfile(self.configs["chrome_driver_path"]): #delete old driver
                    os.remove(self.configs["chrome_driver_path"])

                zfile.extractall(path=self.configs["chrome_driver_path"].replace("chromedriver", ""))

        os.chmod(self.configs["chrome_driver_path"], 0o755) ##change mode to excutable

        self.configs["chrome_driver_version"] = version  # save version it will be used in user-agent

        print("Driver downloaded and extracted at {}".format(self.configs["chrome_driver_path"]))