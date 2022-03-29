from typing import Union
import time
import operate
import pyautogui as pag


class KonosubaScript(operate.Operate):
    '''このファン腳本'''

    def __init__(self) -> None:
        super().__init__()

    def _waitLoading(self) -> None:
        '''等待Loading'''
        timeout = time.perf_counter()+1
        while not self._find('loading'):
            if time.perf_counter() > timeout:
                break
            time.sleep(self.loopPause)
        timeout = time.perf_counter()+1
        while self._find('loading'):
            if time.perf_counter() > timeout:
                break
            time.sleep(self.loopPause)

    def _waitBattleEnd(self) -> None:
        '''等待戰鬥結束'''
        while not self._find('fighting'):
            time.sleep(self.loopPause)
        while self._find('fighting'):
            time.sleep(self.loopPause)

    def _select_team(self, team) -> None:
        '''選擇隊伍'''
        if not self._find('go'):
            return False
        teamNumber = {'team_battle_arena_normal': 0,
                      'team_battle_arena_ex': 1,
                      'team_event': 2}
        c = 0
        for t in teamNumber.keys():
            if self._find(t):
                c = teamNumber[t]-teamNumber[team]
                coordinate = pag.locateCenterOnScreen(
                    self._pic[t], confidence=0.75)
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

    def goAdventure(self) -> bool:
        '''移動到戰鬥'''
        if self._find('adventure_0'):
            self._click('adventure_0')
            return True
        elif self._find('adventure_1'):
            self._click('adventure_1')
            return True
        return False

    def battleArenaLoop(self) -> bool:
        '''刷競技場'''
        def battleArena(mode):
            if self._waitClick(f'battle_arena_{mode}_0', wait=0):
                self._waitLoading()
            if self._find('no_challenge'):
                return False
            self._waitClick('ok', wait=0)
            self._waitClick('challenge')
            if mode == 'normal':
                self._waitClick('advanced', delay=0.5)
            elif mode == 'ex':
                self._waitClick('battle_arena_ex', delay=0.5)
            self._waitClick('ready', delay=0.5)
            self._select_team(f'team_battle_arena_{mode}')
            self._waitClick('go')
            while True:
                self._waitLoading()
                refresh = False
                while True:
                    if self._find('refresh'):
                        refresh = True
                        break
                    if self._find('next'):
                        refresh = False
                        break
                    time.sleep(self.loopPause)
                if self._waitClick('refresh', wait=1, delay=1):
                    print('刷新')
                    time.sleep(1)
                    pag.click()
                    time.sleep(1)
                    pag.click()
                self._waitClick('next', delay=2)
                self._waitClick('next', delay=1.5)
                if refresh and mode == 'normal':
                    self._waitClick('next', delay=1.5)
                self._waitClick('ok', wait=1)
                self._waitClick('again')
                if not self._waitClick('ok', wait=0.5):
                    break
            self._waitClick('next')
            return True

        self.goAdventure()  # 戰鬥
        self._waitClick('battle_arena')  # 競技場
        self._waitLoading()

        battleArena('normal')
        battleArena('ex')

    def eventBossLoop(self, firstDelay) -> None:  # 活動迴圈
        '''刷活動BOSS'''

        def eventBoss(delay, printChange=True) -> float:  # 跑一次活動
            '''傳入等待時間,等待後嘗試再來一局,並回傳下次延遲時間,如無法再來一局回傳-1'''
            print(f"延遲{delay:.1f}秒")
            time.sleep(delay)

            print('準備下一場\n')
            readyTime = time.perf_counter()

            clicked = self._waitClick('go', 'again', 'dead_again', delay=2)
            if clicked == 'go':
                return True
            if not self._waitClick('ok', wait=1):
                return -1

            waited = time.perf_counter()-readyTime-2
            if waited <= 2.5:
                change = -5
            else:
                change = (time.perf_counter()-readyTime-2)/2
            delay += change

            if printChange:
                print(f"等待{waited:.1f}秒")
                print(f'延遲變更{change:.1f}秒')
            return delay

        self._select_team('team_event')

        try:
            keepRun = eventBoss(int(firstDelay), False)

        except ValueError:
            keepRun = eventBoss(0, False)
        nowDelay = 60  # 首次預設延遲
        if keepRun:
            while True:
                if nowDelay == -1:
                    break
                nowDelay = eventBoss(nowDelay)

        self._waitClick('next', delay=1)
        self._waitClick('back', delay=0.5)

    def eventAdventureLoop(self) -> None:
        '''刷新活動關卡'''
        while True:
            self._waitClick('next', delay=1.5)
            self._waitClick('next', delay=2)
            self._waitLoading()
            self._waitLoading()
            self._waitLoading()
            self._waitClick('watch_later', wait=1)
            if not self._waitClick('ready'):
                break
            self._select_team('team_event')
            self._waitClick('go')

    def goHome(self) -> bool:
        '''回主畫面'''
        if self._find('home_0'):
            self._waitClick('home_0')
        elif self._find('home_1'):
            self._waitClick('home_1')
        return False

    def goJob(self) -> None:
        '''到打工畫面'''
        self._waitClick('job')
        self._waitClick('all_receive')
        self._waitClick('ok')
