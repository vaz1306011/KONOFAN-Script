def main():
    print('正在載入模組...')
    from konofanScript import KonofanScript
    ks = KonofanScript()
    from os import system
    system('cls')
    try:
        key = input('(1)刷活動小關卡 (2)刷活動boss (3)刷競技場:')
        if key == '0':
            pass
        elif key == '1':
            ks.eventAdventureLoop()
        elif key == '2':
            firstDelay = input('首次延遲(直接Enter=0s):')
            ks.eventBossLoop(firstDelay)
        elif key == '3':
            ks.battleArenaLoop()
        else:
            print("輸入錯誤")
    except KeyboardInterrupt:
        print('程式結束')


if __name__ == "__main__":
    main()
