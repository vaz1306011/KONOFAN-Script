import json
import threading
from collections import namedtuple
from functools import partial
from pathlib import Path
from time import perf_counter, sleep
from typing import Iterable, Union, overload

import pyautogui as pag
import win32api
import win32con
import win32gui
from PIL import ImageGrab

# 讓螢幕截圖可以用在所有螢幕上
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

FAILSAFE: bool = True  # 安全防護
DEFALUT_CONFIDENCE: float = 0.9  # 預設搜尋精準度
DEFAULT_LOOP_PAUSE: float = 0.5  # 預設迴圈間隔
PIC_PATH: str  # 圖片表路徑
PIC: dict  # 圖片表


exit_event = threading.Event()


class ExitEventException(Exception):
    ...


class NamedPoint:
    """
    帶名座標類

    """

    def __init__(self, pos: Union["NamedPoint", Iterable], name=None) -> None:
        try:
            self.x, self.y = int(pos.x), int(pos.y)
        except AttributeError:
            self.x, self.y = int(pos[0]), int(pos[1])

        self.name = str(name)

    def __str__(self) -> str:
        return f"{self.name}:({self.x}, {self.y})"

    def __add__(self, other: Union["NamedPoint", Iterable]) -> "NamedPoint":
        try:
            return NamedPoint((self.x + other.x, self.y + other.y), self.name)
        except AttributeError:
            return NamedPoint((self.x + other[0], self.y + other[1]))

    def __sub__(self, other: Union["NamedPoint", Iterable]) -> "NamedPoint":
        try:
            return NamedPoint((self.x - other.x, self.y - other.y), self.name)
        except AttributeError:
            return NamedPoint((self.x - other[0], self.y - other[1]))


class NamedPixelColor(namedtuple("NamedPixelColor", ["name", "color"])):
    ...


def loopPause(pause=DEFAULT_LOOP_PAUSE) -> None:
    """
    等待迴圈延遲並檢查是否結束

    """
    sleep(pause)
    if exit_event.is_set():
        raise ExitEventException("強制結束")


def getCursorPos() -> NamedPoint:
    """
    取得滑鼠座標

    """
    return NamedPoint(win32api.GetCursorPos(), "CursorPos")


def getPixel(point: NamedPoint) -> tuple[int, int, int]:
    """
    取得圖片座標像素顏色

    point: 座標

    """
    return pag.pixel(point.x, point.y)


def setPicPath(path: str) -> None:
    """
    設定圖片表路徑

    path: 圖片表路徑

    """
    global PIC_PATH, PIC
    if Path(path).is_absolute():
        PIC_PATH = path
    else:
        PIC_PATH = Path(path).resolve().as_posix()

    try:
        with open(PIC_PATH, "r") as picAddress:
            PIC = json.load(picAddress)
    except FileNotFoundError:
        raise Exception("找不到圖片表")


def find(
    *locations: Union[str, NamedPoint],
    confidence: float = DEFALUT_CONFIDENCE,
    centerPixelColor: tuple[NamedPixelColor] = None,
    tolerance: int = 5,
) -> Union[NamedPoint, None]:
    """
    將圖片名稱轉成座標 (如果傳入名稱有找到回傳座標,否則回傳None)

    *locations: 圖片名稱 或 座標
    confidence: 搜尋精準度
    centerPixelColor: 圖片中心像素顏色 tuple(NamedPixelColor(name, color), ...)
    tolerance: 容許誤差

    """
    # 尋找各個點
    point: NamedPoint = None
    for location in locations:
        if isinstance(location, str):
            pagPoint = pag.locateCenterOnScreen(
                PIC[location], grayscale=True, confidence=confidence
            )
            if pagPoint is not None:
                point = NamedPoint(pagPoint, location)
        elif isinstance(location, NamedPoint):
            point = location
        elif type(location) == "pyscreeze.Point":
            point = NamedPoint((location.x, location.y))
        else:
            raise Exception(f"參數型態錯誤({type(location)})")

        if point is not None:
            break
    else:
        return None

    # 顏色處理
    if centerPixelColor is None:
        return point

    for npc in centerPixelColor:
        if point.name == npc.name:
            break
    else:
        return point

    if pag.pixelMatchesColor(point.x, point.y, npc.color, tolerance=tolerance):
        return point

    return None


@overload
def waitFind(
    *locations: Union[str, NamedPoint],
    confidence: float = DEFALUT_CONFIDENCE,
    centerPixelColor: tuple[NamedPixelColor] = None,
    tolerance: int = 5,
):
    ...


def waitFind(*args, **kwargs) -> NamedPoint:
    """
    等待圖片出現

    *locations: 圖片名稱 或 座標
    confidence: 搜尋精準度
    centerPixelColor: 圖片中心像素顏色 tuple(NamedPixelColor(name, color), ...)
    tolerance: 容許誤差

    """
    while True:
        point = find(*args, **kwargs)
        if point:
            break

        loopPause()

    return point


@overload
def click(
    *locations: Union[str, NamedPoint],
    confidence: float = DEFALUT_CONFIDENCE,
    centerPixelColor: tuple[NamedPixelColor] = None,
    tolerance: int = 5,
):
    ...


def click(*locations, **kwargs) -> Union[NamedPoint, None]:
    """
    傳入pic_address中的名稱或是座標並按下

    *location: 圖片名稱 或 座標
    confidence: 搜尋精準度
    centerPixelColor: 圖片中心像素顏色 tuple(NamedPixelColor(name, color), ...)
    tolerance: 容許誤差

    """
    point = find(*locations, **kwargs)

    if point is None:
        return None

    # 獲取原本滑鼠位置
    currentMouse = win32gui.GetCursorPos()
    if FAILSAFE and currentMouse[0] == currentMouse[1] == 0:
        raise Exception("強制結束")

    # 點擊偵測到的圖片
    win32api.SetCursorPos((point.x, point.y))
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0
    )
    sleep(0.05)

    # 滑鼠回原本位置
    win32api.SetCursorPos(currentMouse)

    return point


@overload
def waitClick(
    *locations: Union[str, NamedPoint],
    delay: float = 0,
    wait: float = -1,
    confidence: float = DEFALUT_CONFIDENCE,
    centerPixelColor: tuple[NamedPixelColor] = None,
    tolerance: int = 5,
) -> Union[NamedPoint, None]:
    ...


def waitClick(
    *locations, delay: float = 0, wait: float = -1, **kwargs
) -> Union[NamedPoint, None]:
    """
    等待並按下,時間內有按下回圖片Point,超時則回傳None

    *locations: 圖片名稱 或 座標
    delay: 找到圖片延遲delay秒後按下
    wait: 等待時間 (wait<0 時無限等待 | wait>=0 時如超過等待時間未按下回傳None)
    confidence: 搜尋精準度
    centerPixelColor: 圖片中心像素顏色 tuple(NamedPixelColor(name, color), ...)
    tolerance: 容許誤差

    """
    # 計算超時時間
    if wait >= 0:
        timeout = perf_counter() + wait

    # 循環搜尋
    while True:
        point = find(*locations, **kwargs)
        if point is not None:
            break

        if wait >= 0 and perf_counter() >= timeout:
            return None

        loopPause()

    sleep(delay)
    click(point)
    return point
