from typing import Union
import os.path
from time import perf_counter, sleep
import pyautogui as pag
import json
import win32api
import win32con
import win32gui

# 不知道什麼原理,反正這3條讓我可以在副螢幕上用這個腳本
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

pag.FAILSAFE = True  # 失效安全防護

DEFALUT_CONFIDENCE = 0.9  # 預設搜尋精準度
LOOPPAUSE = 0.5  # 迴圈間隔
PIC = None  # 圖片表


class Point:
    '''
    圖片座標類
    '''
    def __init__(self, name=None,  x: int = None, y: int = None, *, pagPoint: pag.Point = None) -> None:
        self.name = name
        if pagPoint is not None:
            self.x = pagPoint[0]
            self.y = pagPoint[1]
        else:
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        return f'({self.name}:{self.x}, {self.y})'

    def __add__(self, other: Union['Point', tuple]) -> 'Point':
        if type(other) == tuple:
            return Point(x=self.x+other[0], y=self.y+other[1])
        return Point(x=self.x+other.x, y=self.y+other.y)


def setPicPath(path: str) -> None:
    '''
    設定圖片表路徑

    path: 路徑
    '''
    global PIC
    if os.path.isfile(path):
        with open(path, 'r') as picAddress:
            PIC = json.load(picAddress)
    else:
        raise Exception('找不到圖片表')


def checkPicPath(fun):
    '''
    檢查圖片表是否存在
    '''
    def rtn(*args, **kwargs):
        if PIC is None:
            raise Exception('圖片表不存在')
        return fun(*args, **kwargs)
    return rtn


@checkPicPath
def find(*locations: Union[str, Point], confidence: float = DEFALUT_CONFIDENCE) -> Union[Point, None]:
    '''
    將圖片名稱轉成座標 (如果傳入名稱有找到回傳座標,否則回傳None)

    locations: 圖片名稱 或 座標
    confidence: 搜尋精準度
    '''
    for location in locations:
        if type(location) == str:
            pagPoint = pag.locateCenterOnScreen(PIC[location], confidence=confidence)
            if pagPoint is not None:
                return Point(location, pagPoint[0], pagPoint[1])
        elif type(location) == Point:
            return location
        elif type(location) == 'pyscreeze.Point':
            return Point(None, location.x, location.y)
        else:
            raise Exception('參數錯誤')
    else:
        return None


@checkPicPath
def click(*locations, confidence: float = DEFALUT_CONFIDENCE) -> None:
    '''
    傳入pic_address中的名稱或是座標並按下

    location: 圖片名稱 或 座標
    confidence: 搜尋精準度
    '''
    point = find(*locations, confidence=confidence)

    if point is None:
        raise Exception("找不到圖片")

    # 獲取原本滑鼠位置
    currentMouse = win32gui.GetCursorPos()

    # 點擊偵測到的圖片
    win32api.SetCursorPos((point.x, point.y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    sleep(0.05)

    # 滑鼠回原本位置
    win32api.SetCursorPos(currentMouse)


@checkPicPath
def waitClick(*locations, delay: float = 0, wait: float = -1, confidence: float = DEFALUT_CONFIDENCE) -> Union[Point, None]:
    '''
    等待並按下,時間內有按下回圖片Point,超時則回傳None

    locations: 圖片名稱 或 座標
    delay: 開頭延遲
    wait: 等待時間 (wait<0 時無限等待 | wait>=0 時如超過等待時間未按下回傳None)
    confidence: 搜尋精準度
    '''
    sleep(delay)
    # 計算超時時間
    if wait >= 0:
        timeout = perf_counter()+wait
    # 循環搜尋
    while True:
        point = find(*locations, confidence=confidence)
        # print(point)
        if point is not None:
            break
        if wait >= 0 and perf_counter() >= timeout:
            return None
        sleep(LOOPPAUSE)
    click(point)
    return point
