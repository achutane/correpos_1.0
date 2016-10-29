#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from initsheet import initSheet
from drivesheet import driveSheet

# --- 定数 ---

APPNAME = "CORREPOS"
VERSION = "0.0.1"

#WINDOW_SIZE = (1200, 600)

# --- ウィンドウ ---
class myWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ウィンドウ設定
        self.setWindowTitle(APPNAME)                        # キャプション
#        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])    # サイズ
#       self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        # シート作成
        self.sheets = []
        self.sheets.append(initSheet)	# クラスを登録
        self.sheets.append(driveSheet)
        
        self.sheet = self.sheets[0](self)	# 登録したクラスから1つ選んでインスタンス化
        self.sheet.start()
        
        # ウィンドウ表示
        self.show()
        self.setFixedSize(self.width(), self.height() )		# サイズ固定
        
    # シート切り替え
    def setSheet(self, num):
        self.sheet.stop()	# 終了
        self.sheet = self.sheets[num](self)	# インスタンス化
        self.sheet.start()	# 開始
        
        # ウィンドウ調整
        g0 = self.frameGeometry()
        
        self.setMinimumSize(0,0)
        self.setMaximumSize(10000,10000)
        self.adjustSize()									# サイズ調整
        self.setFixedSize(self.width(), self.height())		# サイズ固定
        # 位置調整
        g1 = self.frameGeometry()
        x = max(0, g1.x() - (g1.width()-g0.width())/2 )
        y = max(0, g1.y() - (g1.height()-g0.height())/2 )
        self.move(x, y)
        

# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = myWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
