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
        while True:
            try:
                period = clearInput('(1) 點到商品頁面\n(2) 在底下輸入你要過幾秒刷新一次網頁\n(3) 接著就會看到頁面重複刷新直到成功將商品放入購物車\n請輸入網頁更新週期(EX: 0.3，可以選擇留白直接按空白，就會採用預設值=0.1): ').strip()
                if len(period) == 0:
                    period = 0.1
                else:
                    period = float(period)
            except Exception as e:
                print(e)
                continue
            else:
                break
                
        shoppingSite.addToCart(period)        
        shoppingSite.checkOut()
        shoppingSite.fillOutCheckoutForm()
if __name__ == "__main__":
    main()