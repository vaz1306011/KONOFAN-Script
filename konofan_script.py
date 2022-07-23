import script as sc


def main():
    print('正在載入模組...')
    try:
        key = input('(1)刷活動小關卡 (2)刷活動Boss (3)刷競技場:')
        if key == '0':
            ...

        elif key == '1':
            sc.eventAdventureLoop()

        elif key == '2':
            firstDelay = input('首次延遲(預設0秒):')
            sc.eventBossLoop(firstDelay)

        elif key == '3':
            sc.battleArenaLoop()

        else:
            print("輸入錯誤")

    except KeyboardInterrupt:
        print('程式結束')


if __name__ == "__main__":
    main()
