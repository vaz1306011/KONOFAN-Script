from base import *
finish_shutdown = False


def main():
    key = input('(1)刷活動小關卡 (2)刷活動boss (3)刷競技場:')
    if key == '1':
        event_adventure_loop()
    elif key == '2':
        event_boss_loop(input('首次延遲:'))
    elif key == '3':
        battle_arena_loop()
    else:
        pass
    if finish_shutdown:
        from os import system
        system("shutdown -s -t 15")


if __name__ == "__main__":
    main()
