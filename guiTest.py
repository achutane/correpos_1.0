#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_W = 1200
WINDOW_H = 600

TXT_CAP = "撮影"
TXT_RECAP = "再撮影"

TXT_NEXT = "次へ"

class myWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# ウィンドウ設定
		self.setWindowTitle(APPNAME)			# キャプション
#		self.move(300,100)						# 位置
		self.setFixedSize(WINDOW_W, WINDOW_H)	# サイズ

		# 撮影ボタン
		self.capButton = QPushButton(TXT_CAP, self)			# 生成、キャプション
		self.capButton.clicked.connect(self.on_clicked_cap)	# クリック時の動作
		self.capButton.resize(self.capButton.sizeHint() )	# サイズ設定
		self.capButton.move(50,50)							# 位置
		
		# Nextボタン
		self.nextButton = QPushButton(TXT_NEXT, self)			# 生成
		self.nextButton.clicked.connect(self.on_clicked_next)	# クリック時
		self.nextButton.resize(self.nextButton.sizeHint() )		# サイズ
		self.nextButton.move(50, 100)							# 配置
		self.nextButton.setEnabled(False)						# 無効化
		
		# ウィンドウ表示
		self.show()

	# 撮影ボタンの動作
	def on_clicked_cap(self):
		self.capButton.setText(TXT_RECAP)	# テキスト変更
		# ToDo カメラ映像キャプチャ
		self.nextButton.setEnabled(True)	# ToDo "次へ"ボタン有効化
		
		
	# Nextボタンの動作
	def on_clicked_next(self):
		# 処理
		print("hello")


def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()