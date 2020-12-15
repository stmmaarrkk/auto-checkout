from datetime import datetime, timedelta
import readline
import time
from util.clearIO import clearPrint, clearInput

class ActivityScheduler:
    def __init__(self):
        self.targetTime = None
    def queryTargetTime(self):
        curTime = datetime.now()
        timeDefault = "{}-{}-{} {}:{}:{}".format(curTime.year, curTime.month, curTime.day,
                                                 curTime.hour, curTime.minute, curTime.second)
        while True:
            try:
                timeStr = rlinput("請設定搶商品日期( 西元年-月-日 時:分:秒 ): ", prefill=timeDefault)
                self.targetTime = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print(e)
                print('確認日期是否有用正確的分割符(包含空白)隔開')
            else:
                print("目標時間為：{}".format(str(self.targetTime)))
                if input("按下Enter繼續或輸入任何字修改目標時間... ") == "":
                    break
    def waiting(self, delay=0.5, period=0.5):
        clearPrint('現在請靜靜等到目標時間，並確保：....\n'
                   '(1) 網頁保持在 "追蹤清單" 頁面\n'
                   '(2) 滑鼠不要亂點(最好是點在程式的這個視窗裡面就好)\n'
                   '(3) 在搶商品時，還沒自動輸入完結帳資訊前請勿亂點')
        while (self.targetTime- datetime.now()).total_seconds() > delay:
            time.sleep(period)
        

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return clearInput(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()
