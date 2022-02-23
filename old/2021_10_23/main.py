import json
import os
import time

import pyautogui as pag

finish_shutdown = True
pag.FAILSAFE = True
pag_confidence = 0.9

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


def find(location, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    if pag.locateCenterOnScreen(pic[location], confidence=confidence, grayscale=True):
        return 1
    return 0


def Click(location: str, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    pag.click(pag.locateCenterOnScreen(
        pic[location], confidence=confidence, grayscale=True))


def wait_fighting():
    while not find('fighting'):
        time.sleep(0.5)
    while find('fighting'):
        time.sleep(0.5)


def wait_click(location: str, delay=0, wait=None, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    if wait != None:
        timeout = time.time()+wait
    while find('loading'):
        time.sleep(0.5)
    while not find(location, confidence=confidence):
        if wait != None and time.time() > timeout:
            return 0
    time.sleep(delay)
    Click(location, confidence=confidence)
    return 1


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
        return 1
    elif find('adventure_1'):
        Click('adventure_1')
        return 1
    return 0


def battle_arena_loop():  # 競技場
    def battle_arena(mode):
        if wait_click(f'battle_arena_{mode}_0', wait=0):
            wait_loading()
        if find('no_challenge'):
            return 0
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
        return 1

    adventure()  # 戰鬥
    wait_click('battle_arena')  # 競技場
    wait_loading()
    # battle_arena('normal')

    battle_arena('ex')


def event_boss_loop():  # 活動迴圈
    run_time = 0
    delay = 60

    def event_boss():  # 跑一次活動
        nonlocal delay, run_time
        run_time += 1
        print(f"延遲{delay:.1f}秒")
        time.sleep(delay)
        ready_time = time.time()
        print('準備下一場')
        wait_click('again', delay=2)
        delay = (delay*run_time+(time.time()-ready_time)-2)/run_time
        if time.time()-ready_time-2 < 0.1:
            delay -= 1
        return wait_click('ok', wait=1)

    while True:
        if not event_boss():
            break
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
    return 0


def job():
    wait_click('job')
    wait_click('all_receive')
    wait_click('ok')


def main():
    key = input('(1)刷活動小關卡 (2)刷活動boss (3)刷競技場:')
    if key == '1':
        event_adventure_loop()
    elif key == '2':
        event_boss_loop()
    elif key == '3':
        battle_arena_loop()
    else:
        pass
    '''
    match key:
        case '1':
            event_adventure_loop()
        case '2':
            event_boss_loop()
        case '3':
            battle_arena_loop()
        case _:
            pass
    '''
    if finish_shutdown:
        os.system("shutdown -s -t 10")


if __name__ == "__main__":
    main()
