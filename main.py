from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from model.Momo import Momo
from util.Info import Info
from util.ActivityScheduler import ActivityScheduler
from util.clearIO import clearPrint, clearInput
import os
import json

def main():
    if(input('因為這程式會要求你輸入一些資訊，雖然我不會盜取這些資訊，他們也不會被放到網路上，但如果會害怕個資外流的人，請不要使用....\n輸入 "y" 以繼續...\n輸入其他任意鍵以離開...').lower() != "y"):
        return
    clearPrint("請確認有下載最新的Chrome driver再使用此程式")
    configFile = "./configs/browser_configs.json"
    configs = {}
    if not os.path.isfile(configFile): #if config doesn't exists
        configs["user_agent"] = input('請輸入 "User-Agent" (Ex: Mozilla/5.0 (Macintosh.....):  ').strip()
        configs["chrome_driver_loc"] = input('請輸入 Chrome driver的路徑(Ex: /usr/xxx ):  ').strip()
        with open(configFile, 'w') as f:
            json.dump(configs, f)
    with open(configFile, 'r') as f:
        configs = json.load(f)
        
    
    info = Info()
    info.prepareInfo()

    # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"')
    # chromeDriverDir = "/usr/local/bin/chromedriver"

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('User-Agent="{}"'.format(configs["user_agent"]))
    browser = webdriver.Chrome(executable_path=configs["chrome_driver_loc"], options=chromeOptions)
    
    site = "momo"
    #site = "pchome
    if site == "momo":
        shoppingSite = Momo(browser=browser, info=info)

        if info.autoLogin:
            shoppingSite.login()
        else:
            clearInput('請手動登入網站並按下 "Enter"....')

        #shoppingSite.getItemInfoFromTrackList(itemTag="4836742") 
        shoppingSite.getItemInfoFromTrackList() 
        
        activityScheduler = ActivityScheduler()
        activityScheduler.queryTargetTime()
        activityScheduler.waiting(delay=0.5, period=0.5)

        shoppingSite.goToItemPage()
        shoppingSite.addToCart()
        shoppingSite.checkOut()
        shoppingSite.fillOutCheckoutForm()
if __name__ == "__main__":
    main()