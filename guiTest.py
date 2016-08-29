#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import cv2

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_W = 1200
WINDOW_H = 600

BUTTON_CAP_X = 100
BUTTON_CAP_Y = 500

BUTTON_NEXT_X = 600
BUTTON_NEXT_Y = 500

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
#		self.setFixedSize(WINDOW_W, WINDOW_H)	# サイズ
		self.resize(WINDOW_W, WINDOW_H)

		# 撮影ボタン
		self.capButton = QPushButton(TXT_CAP, self)			# 生成、キャプション
		self.capButton.clicked.connect(self.on_clicked_cap)	# クリック時の動作
		self.capButton.resize(self.capButton.sizeHint() )	# サイズ設定
		self.capButton.move(BUTTON_CAP_X, BUTTON_CAP_Y)							# 位置
		
		# Nextボタン
		self.nextButton = QPushButton(TXT_NEXT, self)			# 生成
		self.nextButton.clicked.connect(self.on_clicked_next)	# クリック時
		self.nextButton.resize(self.nextButton.sizeHint() )		# サイズ
		self.nextButton.move(BUTTON_NEXT_X, BUTTON_NEXT_Y)							# 配置
		self.nextButton.setEnabled(False)						# 無効化

		# 映像ビュワー		
		self.cvCap = cv2.VideoCapture(0)
		
		self.label1 = QLabel(self)
		self.label1.move(100,100)
		self.label1.resize(320,240)
		
		self.label2 = QLabel(self)
		self.label2.move(500,100)
		self.label2.resize(320,240)
		
		
		# ウィンドウ表示
		self.show()

	# 撮影ボタンの動作
	def on_clicked_cap(self):
		self.capButton.setText(TXT_RECAP)	# テキスト変更
		# ToDo カメラ映像キャプチャ
		self.nextButton.setEnabled(True)	# ToDo "次へ"ボタン有効化
		
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.label2.setPixmap(pix)
		
	# Nextボタンの動作
	def on_clicked_next(self):
		# 処理
		print("hello")

	# 再描画イベント
	def paintEvent(self, event):
		ret, self.frame = self.cvCap.read()
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.label1.setPixmap(pix)

	

def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()