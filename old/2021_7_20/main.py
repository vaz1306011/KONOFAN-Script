import pyautogui as pag
import time

pag.FAILSAFE = True

pag_confidence = 0.9

pic = {'loading': 'loading.png',
       'ok': 'ok.png',
       'next': 'next.png',
       'back': 'back.png',
       'watch_later': 'watch_later.png',
       # 選單
       'home_0': r'home\home_0.png',  # 主畫面0
       'home_1': r'home\home_1.png',  # 主畫面1
       'adventure_0': r'adventure\adventure_0.png',  # 戰鬥0
       'adventure_1': r'adventure\adventure_1.png',  # 戰鬥1

       # 戰鬥
       'fighting': r'adventure\fighting.png',
       'again': r'adventure\again.png',  # 再戰
       'ready': r'adventure\ready.png',  # 準備
       'go': r'adventure\go.png',  # 開始
       # 隊伍
       'team_battle_arena_normal': r'adventure\battle_arena\normal\team_battle_arena_normal.png',
       'team_battle_arena_ex': r'adventure\battle_arena\ex\team_battle_arena_ex.png',
       'team_event': r'adventure\event\team_event.png',
       'left': r'adventure\left.png',
       'right': r'adventure\right.png',
       # 競技場
       'battle_arena': r'adventure\battle_arena\battle_arena.png',
       'challenge': r'adventure\battle_arena\challenge.png',  # 挑戰
       'no_challenge': r'adventure\battle_arena\no_challenge.png',  # 挑戰次數0
       'refresh': r'adventure\battle_arena\refresh.png',  # 成績刷新
       'practice': r'adventure\battle_arena\practice.png',
       # 普通競技場
       'battle_arena_normal_0': r'adventure\battle_arena\normal\battle_arena_normal_0.png',
       'battle_arena_normal_1': r'adventure\battle_arena\normal\battle_arena_normal_1.png',
       'advanced': r'adventure\battle_arena\normal\advanced.png',  # 高級
       # EX競技場
       'battle_arena_ex_0': r'adventure\battle_arena\ex\battle_arena_ex_0.png',
       'battle_arena_ex_1': r'adventure\battle_arena\ex\battle_arena_ex_1.png',
       'battle_arena_ex': r'adventure\battle_arena\ex\battle_arena_ex.png',  # EX級

       # 打工
       'job': r'home\job\job.png',
       'all_receive': r'home\job\all_receive.png'
       }


def wait_loading():
    while not find(pic['loading']):
        pass
    while find(pic['loading']):
        pass


def find(location, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    if pag.locateCenterOnScreen(location, confidence=confidence, grayscale=True):
        return 1
    return 0


def Click(location: str, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    pag.click(pag.locateCenterOnScreen(
        location, confidence=confidence, grayscale=True))


def wait_fighting():
    while not find(pic['fighting']):
        pass
    while find(pic['fighting']):
        pass


def wait_click(location: str, delay=0, wait=None, confidence=None):
    if confidence == None:
        confidence = pag_confidence
    if wait != None:
        timeout = time.time()+wait
    while find(pic['loading']):
        pass
    while not find(location, confidence=confidence):
        if wait != None and time.time() > timeout:
            return 0
    time.sleep(delay)
    Click(location, confidence=confidence)
    return 1


def select_team(team):
    time.sleep(0.4)
    wait_loading()
    team_number = {pic['team_battle_arena_normal']: 0,
                   pic['team_battle_arena_ex']: 1,
                   pic['team_event']: 2
                   }
    c = 0
    for t in team_number.keys():
        if find(t):
            c = team_number[t]-team_number[team]
            coordinate = pag.locateCenterOnScreen(t, confidence=0.75)
            break

    while True:
        if c > 0:
            pag.click(coordinate+(-2180, 440))
            c -= 1
        elif c < 0:
            pag.click(coordinate+(200, 440))
            c += 1
        else:
            break
        time.sleep(0.2)


def adventure():
    if find(pic['adventure_0']):
        Click(pic['adventure_0'])
        return 1
    elif find(pic['adventure_1']):
        Click(pic['adventure_1'])
        return 1
    return 0


def battle_arena_loop():  # 競技場
    def battle_arena(mode):
        if wait_click(pic[f'battle_arena_{mode}_0'], wait=0):
            wait_loading()
        if find(pic['no_challenge']):
            return 0
        wait_click(pic['ok'], wait=0)
        wait_click(pic['challenge'])
        if mode == 'normal':
            wait_click(pic['advanced'], delay=0.5)
        elif mode == 'ex':
            wait_click(pic['battle_arena_ex'], delay=0.5)
        wait_click(pic['ready'], delay=0.5)
        select_team(pic[f'team_battle_arena_{mode}'])
        wait_click(pic['go'])
        while True:
            wait_loading()
            while not find(pic['refresh']) and not find(pic['next']):
                pass
            if wait_click(pic['refresh'], wait=1, delay=1):
                print('刷新')
                time.sleep(1)
                pag.click()
            wait_click(pic['next'], delay=2)
            wait_click(pic['next'], delay=1.5)
            wait_click(pic['ok'], wait=1)
            wait_click(pic['again'])
            if not wait_click(pic['ok'], wait=0.5):
                break
        wait_click(pic['next'])
        return 1

    adventure()  # 戰鬥
    wait_click(pic['battle_arena'])  # 競技場
    wait_loading()
    # if battle_arena('normal'):
    #     wait_loading()
    battle_arena('ex')


def event_boss_loop():  # 活動迴圈
    def event_boss():  # 跑一次活動
        wait_click(pic['again'], delay=2)
        if wait_click(pic['ok'], wait=1):
            return 1
        return 0

    while True:
        if not event_boss():
            break
        wait_fighting()
    wait_click(pic['next'])
    wait_click(pic['back'], delay=0.5)


def event_adventure_loop():
    while True:
        wait_click(pic['next'], delay=1.5)
        wait_click(pic['next'], delay=2)
        wait_loading()
        wait_loading()
        wait_loading()
        print('loaded')
        wait_click(pic['watch_later'], wait=1)
        wait_click(pic['ready'])
        select_team(pic['team_event'])
        wait_click(pic['go'])


def home():
    if find(pic['home_0']):
        wait_click(pic['home_0'])
    elif find(pic['home_1']):
        wait_click(pic['home_1'])
    return 0


def job():
    wait_click(pic['job'])
    wait_click(pic['all_receive'])
    wait_click(pic['ok'])


if __name__ == "__main__":
    event_boss_loop()
    # battle_arena_loop()
