import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

import script as sc
from Ks_UI import Ks_UI


class Ks_Win(Ks_UI, QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.version = "v0.1.5"
        self.setupUi(self)
        self.btn_connect()
        self.now_event = None

    def btn_connect(self) -> None:
        self.allBtn = [self.EAL_btn, self.EBL_btn, self.BAL_btn]
        self.EAL_btn.clicked.connect(self.clickEAL)
        self.EBL_btn.clicked.connect(self.clickEBL)
        self.BAL_btn.clicked.connect(self.clickBAL)
        self.stop_btn.clicked.connect(self.clickStop)
        self.tray.activated.connect(self.trayClick)

    # 建立執行緒
    def createThread(self, func, *args, **kwargs) -> None:
        class Thread(QThread):
            def __init__(self, func, *args, **kwargs):
                super().__init__()
                self.func = func
                self.args = args
                self.kwargs = kwargs

            def run(self) -> None:
                self.func(*self.args, **self.kwargs)

        if (self.now_event is not None) and (not self.now_event.isFinished()):
            self.now_event.terminate()
            self.now_event.wait()

        self.now_event = Thread(func, *args, **kwargs)
        self.now_event.start()

    # 鎖定所有按鈕
    def lockBtn(self, *btns) -> None:
        for btn in btns:
            btn.setEnabled(False)

    # 解鎖所有按鈕
    def unlockBtn(self, *btns) -> None:
        for btn in btns:
            btn.setEnabled(True)

    # 右上角X按鈕
    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

    # 點擊托盤
    def trayClick(self, reason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    # 刷活動小關卡
    def clickEAL(self) -> None:
        self.createThread(sc.eventAdventureLoop)
        self.lockBtn(*self.allBtn)

    # 刷活動Boss
    def clickEBL(self) -> None:
        delay, ok = QInputDialog.getText(self, "刷活動Boss", "首次延遲(預設0秒):")
        if ok:
            self.createThread(sc.eventBossLoop, delay)
            self.lockBtn(*self.allBtn)

    # 刷競技場
    def clickBAL(self) -> None:
        self.createThread(sc.battleArenaLoop)
        self.lockBtn(*self.allBtn)

    # 停止所有任務
    def clickStop(self) -> None:
        self.now_event.terminate()
        self.now_event.wait()
        self.unlockBtn(*self.allBtn)


if __name__ == "__main__":
    app = QApplication([])
    win = Ks_Win()
    win.show()
    sys.exit(app.exec_())
