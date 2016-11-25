#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from logsheet import logSheet
import config

class LOG(QWidget):

    def __init__(self):
        super().__init__()
        self.logsheet()

    def logsheet(self):

        self.setWindowTitle("CORREPOS")
        self.sheet = []
        self.sheet.append(logSheet(self) )
        self.current = 0
        self.sheet[self.current].start()
        self.show()
        self.setFixedSize( self.width(), self.height() )
        config.trayIcon = QSystemTrayIcon(self)
        config.trayIcon.setIcon(QIcon("man.png"))
        config.trayIcon.show()
# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = LOG()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()