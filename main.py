import pyautogui as pag


def main():
    from konosubaScript import KonosubaScript
    ks = KonosubaScript()
    key = input('(1)刷活動小關卡 (2)刷活動boss (3)刷競技場:')
    if key == '0':
        ks.goHome()
        # n=pag.locateCenterOnScreen(
        #     "picture/adventure/adventure_0.png", confidence=0.9, grayscale=True)
        # pag.click(n)
    elif key == '1':
        ks.eventAdventureLoop()
    elif key == '2':
        firstDelay = input('首次延遲:')
        ks.eventBossLoop(firstDelay)
    elif key == '3':
        ks.battleArenaLoop()
    else:
        print("輸入錯誤")


if __name__ == "__main__":
    main()
