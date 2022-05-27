from time import perf_counter, sleep
import pyautogui as pag
import operate as op
from operate import Point, defalutConfidence
from typing import Union


def waitLoading() -> None:
    '''
    等待Loading
    '''

    timeout = perf_counter()+1
    while not op.find('loading'):
        if perf_counter() > timeout:
            break
        sleep(op.LOOPPAUSE)
    timeout = perf_counter()+1
    while op.find('loading'):
        if perf_counter() > timeout:
            break
        sleep(op.LOOPPAUSE)


def waitBattleEnd() -> None:
    '''
    等待戰鬥結束
    '''

    while not op.find('fighting'):
        sleep(op.LOOPPAUSE)
    while op.find('fighting'):
        sleep(op.LOOPPAUSE)


def select_team(team: str) -> None:
    '''
    選擇隊伍
    team: 隊伍名稱
    '''

    if not op.find('go'):
        return False
    teamNumber = {'team_battle_arena_normal': 0,
                  'team_battle_arena_ex': 1,
                  'team_event': 2}
    c = 0
    for t in teamNumber.keys():
        if op.find(t):
            c = teamNumber[t]-teamNumber[team]
            labelPoint = Point(pagPoint=pag.locateCenterOnScreen(op.PIC[t], confidence=defalutConfidence))
            break

    while True:
        if c == 0:
            break
        if c > 0:
            op.click(labelPoint+(1090, 240))
            c -= 1
        if c < 0:
            op.click(labelPoint+(110, 240))
            c += 1
        sleep(0.2)


def goAdventure() -> bool:
    '''
    移動到戰鬥
    '''

    if op.find('adventure_0'):
        op.click('adventure_0')
        return True
    elif op.find('adventure_1'):
        op.click('adventure_1')
        return True
    return False


def battleArenaLoop() -> bool:
    '''
    刷競技場
    '''

    def battleArena(mode):
        if op.waitClick(f'battle_arena_{mode}_0', wait=0):
            waitLoading()
        if op.find('no_challenge'):
            return False
        op.waitClick('ok', wait=0)
        op.waitClick('challenge')
        if mode == 'normal':
            op.waitClick('advanced', delay=0.5)
        elif mode == 'ex':
            op.waitClick('battle_arena_ex', delay=0.5)
        op.waitClick('ready', delay=0.5)
        select_team(f'team_battle_arena_{mode}')
        op.waitClick('go')
        while True:
            waitLoading()
            refresh = False
            while True:
                if op.find('refresh'):
                    refresh = True
                    break
                if op.find('next'):
                    refresh = False
                    break
                sleep(op.LOOPPAUSE)
            if op.waitClick('refresh', wait=1, delay=1):
                print('刷新')
                sleep(1)
                pag.click()
                sleep(1)
                pag.click()
            op.waitClick('next', delay=2)
            op.waitClick('next', delay=1.5)
            if refresh and mode == 'normal':
                op.waitClick('next', delay=1.5)
            op.waitClick('ok', wait=1)
            op.waitClick('again')
            if not op.waitClick('ok', wait=0.5):
                break
        op.waitClick('next')
        return True

    goAdventure()  # 戰鬥
    op.waitClick('battle_arena')  # 競技場
    waitLoading()

    battleArena('normal')
    battleArena('ex')


def eventBossLoop(firstDelay: Union[str, int]) -> None:  # 活動迴圈
    '''
    刷活動BOSS
    firstDelay: 第一次延遲
    '''

    defalutDelay = 60  # 首次延遲

    def eventBoss(delay, returnDelay=True) -> float:  # 跑一次活動
        '''
        傳入等待時間,等待後嘗試再來一局,並回傳下次延遲時間,如無法再來一局回傳-1
        delay: 等待時間
        printChange: 是否列出等待時間和延遲變更
        '''
        try:
            delay = float(delay)
        except ValueError:
            delay = 0
        print(f"延遲{delay:.1f}秒")
        sleep(delay)

        print('準備下一場\n')
        readyTime = perf_counter()+2
        op.waitClick('go', 'again', 'dead_again', delay=2)
        if op.waitClick('ok', wait=1) is None:
            return -1
        if not returnDelay:
            return

        # 延遲時間計算
        waited = perf_counter()-readyTime
        if waited <= 2.5:
            change = -5
        else:
            change = (perf_counter()-readyTime)/2
        delay += change

        print(f"等待{waited:.1f}秒")
        print(f'延遲變更{change:.1f}秒')
        return delay

    select_team('team_event')
    eventBoss(firstDelay, returnDelay=False)
    nowDelay = defalutDelay
    while True:
        if nowDelay == -1:
            break
        nowDelay = eventBoss(nowDelay)

    op.waitClick('next', delay=1)
    op.waitClick('back', delay=0.5)


def eventAdventureLoop() -> None:
    '''
    刷新活動關卡
    '''

    while True:
        op.waitClick('next', delay=1.5)
        sleep(1)
        op.waitClick('next', delay=2)
        waitLoading()
        waitLoading()
        waitLoading()
        op.waitClick('watch_later', wait=1)
        if not op.waitClick('ready'):
            break
        select_team('team_event')
        op.waitClick('go')


def goHome() -> bool:
    '''
    回主畫面
    '''

    if op.find('home_0'):
        op.waitClick('home_0')
    elif op.find('home_1'):
        op.waitClick('home_1')
    return False


def goJob() -> None:
    '''
    到打工畫面
    '''

    op.waitClick('job')
    op.waitClick('all_receive')
    op.waitClick('ok')
