import re
import time
import win32gui
import win32con
import win32com.client


def _window_enum_callback(hwnd, wildcard):
    '''
    Pass to win32gui.EnumWindows() to check all the opened windows
    把想要置頂的視窗放到最前面，並最大化
    '''
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # 先發送一個alt事件，否則會報錯導致後面的設定無效：pywintypes.error: (0,'SetForegroundWindow','No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # 設定為當前活動視窗
        win32gui.SetForegroundWindow(hwnd)
        # 最大化視窗
        # win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

def focusWindow(window_name:str):
    win32gui.EnumWindows(_window_enum_callback, f".*{window_name}.*")

if __name__ == '__main__':
    yt="YouTube"
    time.sleep(1)
    focusWindow(yt)  # 此處為你要設定的活動視窗名
