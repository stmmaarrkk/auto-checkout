# -*- coding: UTF-8 -*-
import json
import os

def getInfoTemplate():
    return {
        "login": {
            "username": "your username",
            "password": "your password"
        },
        "checkout": {
            "birthday": {
                "year": "2000",
                "month": "9",
                "day": "21"
            },
            "mobile": "0912345678",
            "address": {
                "city": "台北市(這邊要填上Momo結帳頁面的下拉式選單有的值)",
                "post": "大安區(這邊要填上Momo結帳頁面的下拉式選單有的值)",
                "full_address": "填完整住址"
            },
            "ID": "A123456789",
            "card": {
                "number": "1234567887654321 (信用卡號 16碼)",
                "expired_year": "2025",
                "expired_month": "07"
            }
        }
    }
def getBrowserConfigs():
    return{
        "chrome_driver_path": "/usr/local/bin/chromedriver", 
        "chrome_driver_version": "", 
        "user_agent": ""}

def main():
    BASEDIR = "./configs/"
    if os.path.isdir(BASEDIR):
        os.system("rm -r {}".format(BASEDIR))
    os.mkdir(BASEDIR)

    with open(BASEDIR + "browser_configs.json", 'w') as f:
        json.dump(getBrowserConfigs(),f)

    with open(BASEDIR+ "info_template.json", 'w') as f:
        json.dump(getInfoTemplate(),f)

if __name__ == "__main__":
    main()
