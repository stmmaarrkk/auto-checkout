from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from util.clearIO import clearPrint, clearInput

class Momo:
    def __init__(self, browser, info):
        self.browser = browser
        self.info = info

        self.homeURL = "https://www.momoshop.com.tw/main/Main.jsp"
        self.browser.get(self.homeURL) 

        self.itemTag = None
    
    def login(self):
        # driver.find
        wait = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='CL1']//a[@id='LOGINSTATUS']")))
        self.browser.find_element_by_xpath("//span[@class='CL1']//a[@id='LOGINSTATUS']").click()

        # password
        print("Login attempt...")
        wait = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, "passwd_show")))
        self.browser.find_element_by_id("passwd_show").click()

        print("passwd_block")
        blankPassword = self.browser.find_element_by_id("passwd")
        blankPassword.clear
        blankPassword.send_keys(self.info.loginInfo["password"])

        # username
        print("usrname")
        blankUserame = self.browser.find_element_by_xpath("//input[@id='memId']")
        blankUserame.clear
        blankUserame.send_keys(self.info.loginInfo["username"])

        self.browser.find_element_by_class_name("loginBtn").click()











        # maxRetry = 2
        # first = True
        # for i in range(maxRetry+1):
        #     if i == maxRetry:
        #         input('失敗次數過多，請手動登入後，按 "Enter"繼續....')
        #         break
        #     try:
        #         #password
        #         print("Login attempt...")
        #         if first:
        #             wait = WebDriverWait(self.browser, 5).until(
        #                 EC.visibility_of_element_located((By.ID, "passwd_show")))
        #             self.browser.find_element_by_id("passwd_show").click()
        #             first = False
        #         else:
        #             try:
        #                 print("passwd_show")
        #                 self.browser.find_element_by_id("passwd_show").click()
        #             except:
        #                 pass
        #
        #         print("passwd_block")
        #         blankPassword = self.browser.find_element_by_id("passwd")
        #         blankPassword.clear
        #         blankPassword.send_keys(self.info.loginInfo["password"])
        #
        #         #username
        #         print("usrname")
        #         blankUserame = self.browser.find_element_by_xpath("//input[@id='memId']")
        #         blankUserame.clear
        #         blankUserame.send_keys(self.info.loginInfo["username"])
        #
        #         self.browser.find_element_by_class_name("loginBtn").click()
        #
        #         #if wait for 1 second, there is still a 註冊(class='CL4') button, then login again
        #         self.browser.implicitly_wait(4)
        #         try:
        #             self.browser.find_element_by_class_name("loginBtn").click()
        #         except:
        #             clearPrint("Login succeeded!")
        #             self.browser.implicitly_wait(0.5)
        #             break
        #         else:
        #             raise Exception
        #     except:
        #         continue
        
    def getItemInfoFromTrackList(self):
        """
        Redirect to wish list using the topbar
        """

        print("Accessing track list...")
        #a element cover this thing, so we have to split click into 2-step
        wait = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@title='追蹤清單']")))
        element = self.browser.find_element_by_xpath("//a[@title='追蹤清單']") 
        self.browser.execute_script("arguments[0].click();", element)
        print("Track list accessed")

        while True:
            try:
                self.itemTag = input("輸入商品編號(追蹤清單裡面會顯示): ").replace(" ", "")
                #self.itemTag = "4836742"#for testing
                
                #ensure the item exists
                self.browser.find_element_by_xpath("//a[@name='{}' and @target='_blank']".format(self.itemTag))

                break
            except Exception as e:
                print('找不到對應的 "商品編號" 請重新輸入....')
                
    def goToItemPage(self):
        print("Redirecting to item page...")

        representation = "//a[@name='{}' and @target='_blank']".format(self.itemTag)
        wait = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, representation)))
        self.browser.find_element_by_xpath(representation).click()
        self.browser.switch_to_window(self.browser.window_handles[-1])
        print("Item page redirected")
    def addToCart(self, period=0.1):
        self.browser.switch_to_window(self.browser.window_handles[-1]) #switch to the most recent page
        # add to cart
        print("Adding item to cart...")

        representation = "//dd[@id='inCar' and not(contains(@style,'display:none'))]"
        while True:
            try:
                wait = WebDriverWait(self.browser, period).until(
                    EC.visibility_of_element_located((By.XPATH, representation)))
                self.browser.find_element_by_xpath(representation).click()
            except:
                self.browser.refresh()
                print("Page refresh...")
            else:
                print("Item added...")
                break

    def checkOut(self, addToCart=True):
        #switch the last tab
        self.browser.switch_to.window(self.browser.window_handles[-1])

        print("Redirecting to checkout page...")
        #a element cover this thing, so we have to split click into 2-step
        #go to checkout from item page
        wait = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//li[@class='checkoutBtn']/a[1]")))
        element = self.browser.find_element_by_xpath("//li[@class='checkoutBtn']/a[1]") 
        self.browser.execute_script("arguments[0].click();", element)

        #checkout
        wait = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li[@class='checkoutBtn']/a[1]")))
        element = self.browser.find_element_by_xpath("//li[@class='checkoutBtn']/a[1]") 
        self.browser.execute_script("arguments[0].click();", element)
        print("Checkout page directed")

    def fillOutCheckoutForm(self):
        #switch the last tab
        self.browser.switch_to.window(self.browser.window_handles[-1])

        TIMEOUTLIMIT = 1
        print("Filling out checkout info...")

        #fill out card number
        try:
            wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "cardNo")))
            blockCardNums = self.browser.find_element_by_class_name("cardNo").find_elements_by_xpath(".//*")[-4:]
            for i in range(4):
                blockCardNums[i].clear
                blockCardNums[i].send_keys(self.info.checkoutInfo["card"]["number"][4*i:4*i+4]) 

            wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
                    EC.visibility_of_element_located((By.NAME, "cardValidMonth")))
            element = Select(self.browser.find_element_by_name("cardValidMonth"))
            element.select_by_visible_text(self.info.checkoutInfo["card"]["expired_month"])

            wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
                    EC.visibility_of_element_located((By.NAME, "cardValidYear")))
            element = Select(self.browser.find_element_by_name("cardValidYear"))
            element.select_by_visible_text(self.info.checkoutInfo["card"]["expired_year"])
            
            wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
                    EC.visibility_of_element_located((By.NAME, "cardCVV")))
            blockCVV = self.browser.find_element_by_name("cardCVV")
            blockCVV.clear
            blockCVV.send_keys(self.info.checkoutInfo["card"]["security_code"])
        except Exception as e:
            print("付款資訊填寫失敗")
            print(e)


        #fill out birth day
        try:
            wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
                    EC.visibility_of_element_located((By.NAME, "birthYear")))
            element = Select(self.browser.find_element_by_name("birthYear"))
            element.select_by_visible_text(self.info.checkoutInfo["birthday"]["year"])
            
            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #         EC.visibility_of_element_located((By.NAME, "birthMonth")))
            element = Select(self.browser.find_element_by_name("birthMonth"))
            element.select_by_visible_text(self.info.checkoutInfo["birthday"]["month"])
            
            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #         EC.visibility_of_element_located((By.NAME, "birthDay")))
            element = Select(self.browser.find_element_by_name("birthDay"))
            element.select_by_visible_text(self.info.checkoutInfo["birthday"]["day"])

        #fill out mobile phone
            phone = self.info.checkoutInfo["mobile"]
            areaCode, number = phone[:2], phone[2:]

            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #         EC.visibility_of_element_located((By.NAME, "defReceiverDDD")))
            blockAreaCode = self.browser.find_element_by_name("defReceiverDDD")
            blockAreaCode.clear
            blockAreaCode.send_keys(areaCode)

            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #         EC.visibility_of_element_located((By.NAME, "defReceiverTel")))
            blockNumber = self.browser.find_element_by_name("defReceiverTel")
            blockNumber.clear
            blockNumber.send_keys(number)

        #fill out address
            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #     EC.visibility_of_element_located((By.NAME, "defReceiverCity")))
            element = Select(self.browser.find_element_by_name("defReceiverCity"))
            element.select_by_visible_text(self.info.checkoutInfo["address"]["city"])
        
            # wait = WebDriverWait(self.browser, TIMEOUTLIMIT).until(
            #     EC.visibility_of_element_located((By.NAME, "defReceiverPost")))
            element = Select(self.browser.find_element_by_name("defReceiverPost"))
            element.select_by_visible_text(self.info.checkoutInfo["address"]["post"])
        
            blockAddress= self.browser.find_element_by_name("defReceiverAddr")
            blockAddress.clear
            blockAddress.send_keys(self.info.checkoutInfo["address"]["full_address"])

        #fill out ID
            blockId= self.browser.find_element_by_name("residentNo")
            blockId.clear
            blockId.send_keys(self.info.checkoutInfo["ID"])

        #check the receiver box
            self.browser.implicitly_wait(0.2)
            self.browser.find_element_by_xpath("//input[@receiver_type='01']").click()

        except Exception as e:
            print("基本資訊填寫失敗")
            print(e)

        print("Checkout info completed")

        clearPrint("請確認結帳資料無誤後輸入信用卡安全碼並結帳，祝你搶到想要的商品!!!")
        while True:
            try:
                assert(input('結帳成功後輸入 "exit" 以離開程式(結帳成功前都不能離開唷)....\n').lower() == "exit")
            except:
                continue
            else:
                break
                
