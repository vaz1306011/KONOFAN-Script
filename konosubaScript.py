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
        time.sleep(0.4)
        self._waitLoading()
        team_number = {'team_battle_arena_normal': 0,
                       'team_battle_arena_ex': 1,
                       'team_event': 2}
        c = 0
        for t in team_number.keys():
            if self._find(t):
                c = team_number[t]-team_number[team]
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

    def goAdventure(self) -> None:
        '''移動到戰鬥'''
        if self._find('adventure_0'):
            self._click('adventure_0')
            return True
        elif self._find('adventure_1'):
            self._click('adventure_1')
            return True
        return False

    def battleArenaLoop(self) -> None:
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

    def eventBossLoop(self, first_delay) -> None:  # 活動迴圈
        '''刷活動BOSS'''
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
                if waited <= 2.5:
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
            self._waitClick('again', 'dead_again', delay=2)
            return self._waitClick('ok', wait=1)

        while event_boss():
            pass
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

    def goHome(self) -> None:
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
