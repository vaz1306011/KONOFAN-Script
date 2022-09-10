import threading
from os import _exit
from threading import Thread

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import script as sc
from Ks_UI import Ks_UI


def excepthook(args):
    raise args[0](args[1])


threading.excepthook = excepthook


class Tray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__()
        self.setIcon(QIcon("icon.ico"))
        self.setToolTip("Konofan")

        self.menu = QMenu()
        self.menu.addAction("還原主視窗", parent.show)
        self.menu.addAction("結束", lambda: _exit(0))
        self.setContextMenu(self.menu)


class Ks_Win(Ks_UI, QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.tray = Tray(self)
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

    # 關閉程式
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        # exit(0)
        # msBox = QMessageBox(0, '確認', '確定要結束程式嗎?', QMessageBox.Yes | QMessageBox.No, self)
        # msBox.button(QMessageBox.Yes).setText('是')
        # msBox.button(QMessageBox.No).setText('否')
        # click = msBox.exec()
        # if click == QMessageBox.Yes:
        #     _exit(0)
        # else:
        #     event.ignore()

    # 托盤點擊
    def trayClick(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def createThread(self, func, *args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.start()

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
        sc.op.exit_event.set()
        self.unlockBtn(*self.allBtn)


if __name__ == "__main__":
    app = QApplication([])
    win = Ks_Win()
    win.show()
    app.exec_()
