from os import _exit
import threading
from threading import Thread

from PyQt5.QtWidgets import *

import konofanScript as ks
from Ks_UI import Ks_UI


def excepthook(args):
    raise args[0](args[1])


threading.excepthook = excepthook


class Ks_Win(Ks_UI, QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.allBtn = [self.EAL_btn, self.EBL_btn, self.BAL_btn]
        self.EAL_btn.clicked.connect(self.clickEAL)
        self.EBL_btn.clicked.connect(self.clickEBL)
        self.BAL_btn.clicked.connect(self.clickBAL)
        self.stop_btn.clicked.connect(self.clickStop)

    # 刷活動小關卡
    def clickEAL(self):
        ks.op.exit_event.clear()
        self.createThread(ks.eventAdventureLoop)
        self.lockBtn(*self.allBtn)

    # 刷活動Boss
    def clickEBL(self):
        ks.op.exit_event.clear()
        delay, ok = QInputDialog.getText(
            self,
            '刷活動Boss',
            '首次延遲(預設0秒):'
        )
        if ok:
            self.createThread(ks.eventBossLoop, delay)
            self.lockBtn(*self.allBtn)

    # 刷競技場
    def clickBAL(self):
        ks.op.exit_event.clear()
        self.createThread(ks.battleArenaLoop)
        self.lockBtn(*self.allBtn)

    # 停止按鈕
    def clickStop(self):
        ks.op.exit_event.set()
        self.unlockBtn(*self.allBtn)

    def createThread(self, func, *args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.start()

    def lockBtn(self, *btns):
        for btn in btns:
            btn.setEnabled(False)

    def unlockBtn(self, *btns):
        for btn in btns:
            btn.setEnabled(True)

    def closeEvent(self, event):
        _exit(0)
        msBox = QMessageBox(0, '確認', '確定要結束程式嗎?', QMessageBox.Yes | QMessageBox.No, self)
        msBox.button(QMessageBox.Yes).setText('是')
        msBox.button(QMessageBox.No).setText('否')
        click = msBox.exec()
        if click == QMessageBox.Yes:
            _exit(0)
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    win = Ks_Win()
    win.show()
    app.exec_()
