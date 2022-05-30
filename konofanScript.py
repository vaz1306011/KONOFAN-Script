from time import perf_counter, sleep
from typing import Union

import pyautogui as pag

import operate as op
from operate import LOOP_PAUSE


def waitLoading() -> None:
    '''
    等待Loading
    '''
    timeout = perf_counter()+1
    while not op.find('loading'):
        if perf_counter() > timeout:
            break

        sleep(LOOP_PAUSE)

    timeout = perf_counter()+1
    while op.find('loading'):
        if perf_counter() > timeout:
            break

        sleep(LOOP_PAUSE)


def waitBattleEnd() -> None:
    '''
    等待戰鬥結束
    '''
    while not op.find('fighting'):
        sleep(LOOP_PAUSE)

    while op.find('fighting'):
        sleep(LOOP_PAUSE)


def select_team(team: str) -> None:
    '''
    選擇隊伍

    team: 隊伍名稱 (team_battle_arena_normal, team_battle_arena_ex, team_event)
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
            point = pag.locateCenterOnScreen(op.PIC[t], confidence=op.DEFALUT_CONFIDENCE)
            teamNamePoint = op.namedPoint((point.x, point.y))
            break

    while True:
        if c == 0:
            break
        elif c > 0:
            op.click(teamNamePoint+(1090, 240))
            c -= 1
        elif c < 0:
            op.click(teamNamePoint+(110, 240))
            c += 1

        sleep(LOOP_PAUSE)


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

                sleep(LOOP_PAUSE)

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
    DEFAULT_DELAY = 60  # 預設平均延遲

    def eventBoss() -> int:  # 跑一次活動
        '''
        跑一次活動(回傳 1:正常運行, 0:需重製預設延遲, -1:無法繼續)
        '''
        button = op.waitFind('next', 'go')
        if button.name == 'go':
            op.click(button.name)
            return 0
        else:
            againColor = op.NamedPixelColor('again', (157, 149, 140))
            click = op.waitClick('again', 'dead_again', wait=2, centerPixelColor=(againColor,))

        if click is None:
            op.waitClick('next', wait=1)
            return -1

        op.waitClick('ok')
        if click.name == 'dead_again':
            return 0

        return 1

    select_team('team_event')
    try:
        delay = float(firstDelay)
    except ValueError:
        delay = 0

    print(f"延遲{delay:.1f}秒")
    sleep(delay)
    eventBoss()
    delay = DEFAULT_DELAY
    print(f"預設延遲設為{DEFAULT_DELAY}秒")

    while True:
        print(f"延遲{delay:.1f}秒")
        sleep(delay)

        print('準備下一場\n')
        readyTime = perf_counter()

        eventBossRtn = eventBoss()
        if eventBossRtn == 0:
            delay = DEFAULT_DELAY
            print(f"預設延遲設為{DEFAULT_DELAY}秒")
            continue
        elif eventBossRtn == -1:
            break

        # 延遲時間計算
        waited = perf_counter()-readyTime
        if waited <= 2.5:
            change = -5
        else:
            change = (perf_counter()-readyTime)/2

        delay += change

        print(f"等待{waited:.1f}秒")
        print(f'延遲變更{change:.1f}秒')

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
