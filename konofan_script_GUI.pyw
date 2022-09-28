import sys

from PyQt5.QtCore import QCoreApplication, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import script as sc
from Ks_UI import Ks_UI




class Tray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__()
        self.setIcon(QIcon("icon.ico"))
        self.setToolTip("KonofanScript")

        self.menu = QMenu()
        self.menu.addAction("還原主視窗", parent.show)
        self.menu.addAction("結束", QCoreApplication.instance().quit)
        self.setContextMenu(self.menu)


class Ks_Win(Ks_UI, QFrame):
    class Thread(QThread):
        def __init__(self, func, *args, **kwargs):
            super().__init__()
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def run(self) -> None:
            self.func(*self.args, **self.kwargs)

    def __init__(self) -> None:
        super().__init__()
        self.version = "0.1.3"
        self.initUI()
        self.now_event = None

        self.tray = Tray(self)
    def initUI(self):
        self.version = "v0.1.4"

        self.tray = self.Tray(self)
        self.tray.show()
        self.tray.activated.connect(self.trayClick)

        self.icon = QIcon("icon.ico")
        self.setWindowIcon(self.icon)

        self.setupUi(self)
        self.allBtn = [self.EAL_btn, self.EBL_btn, self.BAL_btn]
        self.EAL_btn.clicked.connect(self.clickEAL)
        self.EBL_btn.clicked.connect(self.clickEBL)
        self.BAL_btn.clicked.connect(self.clickBAL)
        self.stop_btn.clicked.connect(self.clickStop)

    # 托盤點擊
    def trayClick(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    # 建立執行緒
    def createThread(self, func, *args, **kwargs):
        self.now_event = self.Thread(func, *args, **kwargs)
        self.now_event.start()

    def lockBtn(self, *btns):
        for btn in btns:
            btn.setEnabled(False)

    def unlockBtn(self, *btns):
        for btn in btns:
            btn.setEnabled(True)

    # 刷活動小關卡
    def clickEAL(self):
        sc.op.exit_event.clear()
        self.createThread(sc.eventAdventureLoop)
        self.lockBtn(*self.allBtn)

    # 刷活動Boss
    def clickEBL(self):
        sc.op.exit_event.clear()
        delay, ok = QInputDialog.getText(self, "刷活動Boss", "首次延遲(預設0秒):")
        if ok:
            self.createThread(sc.eventBossLoop, delay)
            self.lockBtn(*self.allBtn)

    # 刷競技場
    def clickBAL(self):
        sc.op.exit_event.clear()
        self.createThread(sc.battleArenaLoop)
        self.lockBtn(*self.allBtn)

    # 停止所有任務
    def clickStop(self):
        self.now_event.terminate()
        self.now_event.wait()
        if self.now_event.isFinished():
            self.unlockBtn(*self.allBtn)


if __name__ == "__main__":
    app = QApplication([])
    win = Ks_Win()
    win.show()
    sys.exit(app.exec_())
