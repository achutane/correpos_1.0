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

WINDOW_SIZE = (1200, 600)

BUTTON_SIZE = (100, 23)	# フォント23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_CAP = "撮影"
TXT_RECAP = "再撮影"

TXT_NEXT = "次へ"

class myWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# ウィンドウ設定
		self.setWindowTitle(APPNAME)						# キャプション
#		self.move(300,100)									# 位置
#		self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])	# サイズ
		self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

		# 撮影ボタン
		self.capButton = QPushButton(TXT_CAP, self)					# 生成、キャプション
		self.capButton.clicked.connect(self.on_clicked_cap)			# クリック時の動作
		self.capButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )		# サイズ設定
		self.capButton.move(BUTTON_CAP_POS[0], BUTTON_CAP_POS[1])	# 位置
		
		# Nextボタン
		self.nextButton = QPushButton(TXT_NEXT, self)					# 生成
		self.nextButton.clicked.connect(self.on_clicked_next)			# クリック時
		self.nextButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )				# サイズ
		self.nextButton.move(BUTTON_NEXT_POS[0], BUTTON_NEXT_POS[1])	# 配置
		self.nextButton.setEnabled(False)								# 無効化

		# カメラ		
		self.cvCap = cv2.VideoCapture(0)
		
		# 映像表示
		self.label1 = QLabel(self)
		self.label1.move(IMG1_POS[0], IMG1_POS[1])
		self.label1.resize(IMG_SIZE[0], IMG_SIZE[1])
		
		# スクショ表示
		self.label2 = QLabel(self)
		self.label2.move(IMG2_POS[0], IMG2_POS[1])
		self.label2.resize(IMG_SIZE[0], IMG_SIZE[1])
		
		
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
		print("next")

	# 再描画イベント
	def paintEvent(self, event):
		ret, frame1 = self.cvCap.read()	# キャプチャ
		frame2 = cv2.resize(frame1, IMG_SIZE )	# リサイズ
		frame2 = frame2[:,::-1]

            for rect in facerect:
        #検出した顔を囲む矩形の作成
           cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)
		
		self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)	# 色変換 BGR -> RGB
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)	# QImage生成
		pix = QPixmap.fromImage(img)		# QPixmap生成
		self.label1.setPixmap(pix)			# 画像貼り付け

	

def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()