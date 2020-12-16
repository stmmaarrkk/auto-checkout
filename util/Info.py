import json
import os
from util.clearIO import clearInput, clearPrint

class Info:
    def __init__(self, filename="./configs/info.json", autoLogin=False, autoFillCheckoutInfo=True):
        #define file name
        self.templateName = "./configs/info_template.json"
        self.rawTxtName = "./configs/tmp.txt"
        self.infoName = filename

        #define bool
        self.autoLogin = autoLogin
        self.autoFillCheckoutInfo = autoFillCheckoutInfo

        #info
        self.loginInfo = None
        self.checkoutInfo = None

    def prepareInfo(self):
        result = clearInput('若想開啟自動登入功能，請輸入 "1"，否則請輸入任意字元): ')
        self.autoLogin = True if result == "1" else False
        
        prepareInfoOptions = [" 新增或重新填寫資料"] #0
        if os.path.isfile(self.infoName ):
            prepareInfoOptions.append("修改現有資料") #1
            prepareInfoOptions.append("直接載入現有資料") #2

        #choose initial option
        clearPrint("因為結帳時要自動填入資料", end="")
        if len(prepareInfoOptions) == 1: #only have 1 choice
            choice =  "0"
            print("，所以這邊要填上結帳資料")
        else:
            print("，所以這邊要先輸入結帳資料，你可以執行:")
            for i, opt in enumerate(prepareInfoOptions):
                print("({}) {}".format(i, opt))

            while True:
                try:
                    choice = input("請輸入選項(數字):")
                    assert int(choice) in list(range(len(prepareInfoOptions))), "請輸入合理選項"
                except AssertionError:
                    pass
                else:
                    break
        
        if choice in ["0", "1"]: #input directly
            if os.path.isfile(self.infoName) and choice == "1": #load existed one
                self.load(self.infoName, needValidate=False) 
            else: #load new one
                self.load(self.templateName, needValidate=False)

            while True:
                try:
                    with open(self.rawTxtName, "w") as f:
                        f.write("每個欄位都必須要填唷\n\n")
                        if self.autoLogin:
                            iterateAllDict(self.loginInfo, 
                            lambda k, v, *s: s[0].write("{}: {}\n".format(k, v)), 
                            f)
                        if self.autoFillCheckoutInfo:     
                            iterateAllDict(self.checkoutInfo, 
                            lambda k, v, *s: s[0].write("{}: {}\n".format(k, v)),
                            f)
                        f.write("\n填完儲存完後，關閉此檔案並回到程式視窗")
                    
                    # Mode to be set  
                    os.system("open {}".format(self.rawTxtName))
                    input('填完資料後關閉檔案在此處按 "Enter"....')
                    self.processedRawTxt(remove=True)
                    
                except Exception as e:
                    clearPrint(e)
                    print("請重新填寫")
                    if os.path.isfile(self.infoName): #load existed one
                        self.load(self.infoName, needValidate=False) 
                    else: #load new one
                        self.load(self.templateName, needValidate=False)
                else:
                    print("Info loaded")
                    break

        elif choice is "2":
            self.load(self.infoName)
                    

    def processedRawTxt(self, remove=True):
        if os.path.isfile(self.infoName):
            self.load(self.infoName, needValidate=False)
        else:
            self.load(self.templateName, needValidate=False)

        with open(self.rawTxtName, "r") as f:
            lines = f.readlines()
            lines = lines[2:-2] #remove last 2 lines and first 2 lines 
            for line in lines:
                line = line.replace(" ", "").replace("\n", "")
                key, value = line.split(":")

                for info in [self.loginInfo, self.checkoutInfo]:
                    #search in info
                    result = getElementByKey(info, key)
                    if result:
                        result[key] = value
                        break

        if remove:
            os.remove(self.rawTxtName)

        self.validate()

        ##special validate and processes
        #remove special characters from credit card
        self.checkoutInfo["card"]["number"] = self.checkoutInfo["card"]["number"].replace("-", "").replace(",", "")
        #let preceeding 0 go
        if self.checkoutInfo["birthday"]["month"][0] == "0":
            self.checkoutInfo["birthday"]["month"] = self.checkoutInfo["birthday"]["month"][-1]
        #let preceeding 0 go
        if self.checkoutInfo["birthday"]["day"][0] == "0":
            self.checkoutInfo["birthday"]["day"] = self.checkoutInfo["birthday"]["day"][-1]
        #add preceeding 0
        if len(self.checkoutInfo["card"]["expired_month"]) == 1:
            self.checkoutInfo["card"]["expired_month"] = "0" + self.checkoutInfo["card"]["expired_month"]

        ##dump to info.json
        with open(self.infoName, 'w', encoding='utf-8') as f:
            json.dump({"login":self.loginInfo, "checkout":self.checkoutInfo}, f, ensure_ascii=False, indent=4)
        #reload it to memory
        self.load(self.infoName, needValidate=True)

    def validate(self):
        def checkNull(k, v):
            assert v != "", "{} should not be null".format(k)

        if self.autoLogin: #validate login info
            iterateAllDict(self.loginInfo, checkNull)
        if self.autoFillCheckoutInfo:
            iterateAllDict(self.checkoutInfo, checkNull)
        
    def load(self, filename, needValidate=True):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.loginInfo = data["login"]
            self.checkoutInfo = data["checkout"]
        if needValidate:
            self.validate()
                
def iterateAllDict(nested_dictionary, func, *args):
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            iterateAllDict(value, func, *args)
        else:
            func(key, value, *args)    

def getElementByKey(nested_dictionary, target):
    result = None
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            result = getElementByKey(value, target)
        elif key == target:
            result =  nested_dictionary
        if result:
            return result
