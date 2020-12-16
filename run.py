# -*- coding: UTF-8 -*-
from model.Momo import Momo
from util.ActivityScheduler import ActivityScheduler
from util.Bootstrap import Bootstrap
from util.Info import Info
from util.clearIO import clearPrint, clearInput



def main():
    if(clearInput('因為這程式會要求你輸入一些資訊，雖然我不會盜取這些資訊，他們也不會被放到網路上，但如果會害怕個資外流的人，請不要使用....\n輸入 "y" 以繼續...\n輸入其他任意鍵以離開...').lower() != "y"):
        return

    bootstrap = Bootstrap()
    
    info = Info()
    info.prepareInfo()

    browser = bootstrap.launchBrowser()
    
    site = "momo"
    #site = "pchome
    if site == "momo":
        shoppingSite = Momo(browser=browser, info=info)

        if info.autoLogin:
            shoppingSite.login()
        else:
            clearInput('請手動登入網站並按下 "Enter"....')

        #shoppingSite.getItemInfoFromTrackList(itemTag="4836742") 
        #shoppingSite.getItemInfoFromTrackList() 
        
        # activityScheduler = ActivityScheduler()
        # activityScheduler.queryTargetTime()
        # activityScheduler.waiting(delay=0.5, period=0.5)

        #shoppingSite.goToItemPage()
        if input('點到商品頁面後回來這再按下 "Enter" 就會看到頁面重複刷新直到成功將商品放入購物車') == "test":
            shoppingSite.addToCart(test=True)
        else:
            shoppingSite.addToCart(test=False)
        shoppingSite.checkOut()
        shoppingSite.fillOutCheckoutForm()
if __name__ == "__main__":
    main()