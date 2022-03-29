import time
import pyautogui as pag
import json
from typing import Union
import win32api
import win32con
import win32gui
import autoit

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
        '''按下,可傳入pic_address中的名稱或是座標'''
        if type(location) == str:  # 如果傳入字串把字串轉成位置
            location = pag.locateCenterOnScreen(self._pic[location], confidence=0.9)
        confidence = confidence or self.pag_confidence

        # current_mouse = pag.position()  # 獲取原本滑鼠位置

        currentMouse = win32gui.GetCursorPos()

        # pag.click(location)  # 點擊偵測到的圖片

        win32api.SetCursorPos(location)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.01)

        # pag.moveTo(currentMouse)  # 滑鼠回原本位置

        win32api.SetCursorPos(currentMouse)

    def _find(self, *locations, confidence=None) -> Union[tuple, None]:
        '''尋找圖,如果有找到回傳圖片 名稱[0] 和 位置[1],否則回傳False'''
        confidence = confidence or self.pag_confidence
        for location in locations:
            # print('try', location)
            point = pag.locateCenterOnScreen(self._pic[location], confidence=confidence)
            if point:
                # print('found', location)
                return location, point
        return None

    def _waitClick(self, *locations: str, delay: float = 0, wait: float = -1, confidence: float = None) -> Union[str, None]:
        '''等待並按下,如果有按下回圖片名稱,否則回傳False'''
        if confidence == None:
            confidence = self.pag_confidence
        if wait >= 0:
            timeout = time.perf_counter()+wait
        while self._find('loading'):
            time.sleep(self.loopPause)
        while True:
            try:
                location, point = self._find(*locations, confidence=confidence)
            except TypeError:
                if wait >= 0 and time.perf_counter() > timeout:
                    return None
                time.sleep(self.loopPause)
            else:
                break
        time.sleep(delay)
        self._click(point, confidence=confidence)
        return location


if __name__ == "__main__":
    Operate()
