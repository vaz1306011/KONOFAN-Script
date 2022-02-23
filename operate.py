import time
import pyautogui as pag
import json
# 不知道什麼原理,反正這3條讓我可以在副螢幕上用這個腳本
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


class Operate:
    '''滑鼠功能操作'''

    def __init__(self) -> None:
        pag.FAILSAFE = True  # 失效安全防護
        self.pag_confidence = 0.9  # 預設搜尋精準度
        self.loopPause = 0.5  # 迴圈間隔
        try:
            with open('pic_address.json', 'r') as pic_address:  # 匯入圖片
                self._pic = json.load(pic_address)

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open('pic_address.json', 'w+') as pic_address:
                pic_address.write("{\n\n}")

    def _click(self, location: str, confidence=None) -> None:
        '''按下'''
        if type(location) == str:  # 如果傳入字串把字串轉成位置
            location = pag.locateCenterOnScreen(
                self._pic[location], confidence=0.9)  # , grayscale=True
        if confidence == None:
            confidence = self.pag_confidence
        current_mouse = pag.position()  # 獲取原本滑鼠位置
        pag.click(location)  # 點擊偵測到的圖片
        pag.moveTo(current_mouse)  # 滑鼠回原本位置

    def _find(self, *locations, confidence=None) -> bool:
        '''尋找圖片'''
        if confidence == None:
            confidence = self.pag_confidence
        for location in locations:
            point = pag.locateCenterOnScreen(
                self._pic[location], confidence=confidence)  # , grayscale=True
            if point:
                return point
        return False

    def _waitClick(self, *locations: str, delay: float = 0, wait: float = -1, confidence: float = None) -> bool:
        '''等待並按下'''
        if confidence == None:
            confidence = self.pag_confidence
        if wait >= 0:
            timeout = time.perf_counter()+wait
        while self._find('loading'):
            time.sleep(self.loopPause)
        while True:
            location = self._find(*locations, confidence=confidence)
            if location:
                break
            if wait >= 0 and time.perf_counter() > timeout:
                return False
            time.sleep(self.loopPause)
        time.sleep(delay)
        self._click(location, confidence=confidence)
        return True


if __name__ == "__main__":
    Operate()
