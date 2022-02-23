import json
import time
import win32gui
import pyautogui as pag

# 不知道什麼原理,反正這3條讓我可以在副螢幕上用這個腳本
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

pag.FAILSAFE = True
pag_confidence = 0.9  # 預設搜尋精準度

with open('pic_address.json', 'r') as pic_address:
    pic = json.load(pic_address)


def wait_loading():
    timeout = time.time()+1
    while not find('loading'):
        if time.time() > timeout:
            break
        time.sleep(0.5)
    timeout = time.time()+1
    while find('loading'):
        if time.time() > timeout:
            break
        time.sleep(0.5)


def find(*locations, confidence=None):
    for location in locations:
        if confidence == None:
            confidence = pag_confidence
        if pag.locateCenterOnScreen(pic[location], confidence=confidence, grayscale=True):
            return location
    return False


def Click(location: str, confidence=None):
    current_mouse = pag.position()  # 獲取原本滑鼠位置
    if confidence == None:
        confidence = pag_confidence
    pag.click(pag.locateCenterOnScreen(
        pic[location], confidence=confidence, grayscale=True))  # 點擊偵測到的圖片
    pag.moveTo(current_mouse)  # 滑鼠回原本位置


def wait_fighting():
    while not find('fighting'):
        time.sleep(0.5)
    while find('fighting'):
        time.sleep(0.5)


def wait_click(*locations, delay=0, wait=None, confidence=None):

    if confidence == None:
        confidence = pag_confidence
    if wait != None:
        timeout = time.time()+wait
    while find('loading'):
        time.sleep(0.5)
    while True:
        location = find(*locations, confidence=confidence)
        if location:
            break
        if wait != None and time.time() > timeout:
            return False
        time.sleep(0.5)
    time.sleep(delay)
    Click(location, confidence=confidence)
    return True


def select_team(team):
    time.sleep(0.4)
    wait_loading()
    team_number = {'team_battle_arena_normal': 0,
                   'team_battle_arena_ex': 1,
                   'team_event': 2
                   }
    c = 0
    for t in team_number.keys():
        if find(t):
            c = team_number[t]-team_number[team]
            coordinate = pag.locateCenterOnScreen(pic[t], confidence=0.75)
            break

    while True:
        if c > 0:
            pag.click(coordinate+(-2180, 490))
            c -= 1
        elif c < 0:
            pag.click(coordinate+(200, 490))
            c += 1
        else:
            break
        time.sleep(0.2)


def adventure():
    if find('adventure_0'):
        Click('adventure_0')
        return True
    elif find('adventure_1'):
        Click('adventure_1')
        return True
    return False


def battle_arena_loop():  # 競技場
    def battle_arena(mode):
        if wait_click(f'battle_arena_{mode}_0', wait=0):
            wait_loading()
        if find('no_challenge'):
            return False
        wait_click('ok', wait=0)
        wait_click('challenge')
        if mode == 'normal':
            wait_click('advanced', delay=0.5)
        elif mode == 'ex':
            wait_click('battle_arena_ex', delay=0.5)
        wait_click('ready', delay=0.5)
        select_team(f'team_battle_arena_{mode}')
        wait_click('go')
        while True:
            wait_loading()
            while not find('refresh') and not find('next'):
                time.sleep(0.5)
            if wait_click('refresh', wait=1, delay=1):
                print('刷新')
                time.sleep(1)
                pag.click()
            wait_click('next', delay=2)
            wait_click('next', delay=1.5)
            wait_click('ok', wait=1)
            wait_click('again')
            if not wait_click('ok', wait=0.5):
                break
        wait_click('next')
        return True

    adventure()  # 戰鬥
    wait_click('battle_arena')  # 競技場
    wait_loading()
    # battle_arena('normal')

    battle_arena('ex')


def event_boss_loop(first_delay):  # 活動迴圈
    default_delay = 60
    delay = default_delay

    def count_delay(fun):
        def r_fun():
            nonlocal delay, first_delay

            if first_delay != "":  # 首次延遲設定
                delay = int(first_delay)

            print(f"延遲{delay:.1f}秒")
            time.sleep(delay)
            ready_time = time.perf_counter()
            keep_loop = fun()
            waited = time.perf_counter()-ready_time-2

            if first_delay != "":  # 首次延遲回調
                delay = default_delay
                first_delay = ""
                return keep_loop

            print(f"本次等待{waited:.1f}秒")
            if waited < 1.5:
                change = -5
            else:
                change = (time.perf_counter()-ready_time-2)/2
            print(f'延遲變更{change:.1f}秒')
            delay += change
            return keep_loop
        return r_fun

    @count_delay
    def event_boss():  # 跑一次活動
        print('準備下一場\n')
        wait_click('again', 'dead_again', delay=2)
        return wait_click('ok', wait=1)

    while event_boss():
        time.sleep(0.5)
    wait_click('next', delay=1)
    wait_click('back', delay=0.5)


def event_adventure_loop():
    while True:
        wait_click('next', delay=1.5)
        wait_click('next', delay=2)
        wait_loading()
        wait_loading()
        wait_loading()
        wait_click('watch_later', wait=1)
        if not wait_click('ready'):
            break
        select_team('team_event')
        wait_click('go')


def home():
    if find('home_0'):
        wait_click('home_0')
    elif find('home_1'):
        wait_click('home_1')
    return False


def job():
    wait_click('job')
    wait_click('all_receive')
    wait_click('ok')
