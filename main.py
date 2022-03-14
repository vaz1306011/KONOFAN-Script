def main():
    from konosubaScript import KonosubaScript
    ks = KonosubaScript()
    key = input('(1)刷活動小關卡 (2)刷活動boss (3)刷競技場:')
    if key == '0':
        ks.goHome()
    elif key == '1':
        ks.eventAdventureLoop()
    elif key == '2':
        firstDelay = input('首次延遲(直接Enter=60s):')
        ks.eventBossLoop(firstDelay)
    elif key == '3':
        ks.battleArenaLoop()
    else:
        print("輸入錯誤")


if __name__ == "__main__":
    main()
