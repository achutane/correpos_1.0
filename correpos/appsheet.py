#!/usr/bin/python
# -*- coding: utf-8 -*-

from sheet import sheet
import config

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import datetime
import cv2
import wavplay_pygame
from os.path import join, relpath
from glob import glob
import copy
import pandas as pd
import os.path


# --- 定数 ---
IMG_SIZE = (400, 300)

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# --- 動作中画面 ---
class appSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 画像
        imageSize = QSize(100,100)		# サイズ
        self.image = QImage("man.png").scaled(imageSize)
        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(imageSize)
        self.imageLabel.setPixmap( QPixmap.fromImage(self.image) )
        
        # 各ボタン
        self.recapButton = QPushButton( QIcon("cameraIcon.png"), "")	# 再撮影
        self.recapButton.clicked.connect( self.on_clicked_recap )
        
        self.logButton = QPushButton( QIcon("logIcon.png"), "")			# ログ
        self.logButton.clicked.connect( self.on_clicked_log )
        
        self.settingButton = QPushButton( QIcon("settingIcon.png"), "")	# 設定
        self.settingButton.clicked.connect( self.on_clicked_setting )
        
        # ボタンサイズ設定
        for b in [self.recapButton, self.logButton, self.settingButton]:
            b.setFixedSize(32,32)
        
        # 猫背ゲージ
        self.pbar = QProgressBar()
        self.pbar.setTextVisible(False)	# パーセント表示オフ
        self.pbar.setFixedHeight(8)		# 高さ
        self.pbar.setValue(30)			# 値設定(適当)
        
        # --- 配置 ---
        vb1 = QVBoxLayout()		# 全体
        
        hb1 = QHBoxLayout()		# 画像＋ボタン
        hb1.addWidget( self.imageLabel )	# 画像
        
        vb2 = QVBoxLayout()		# ボタン縦配置
        vb2.addWidget(self.recapButton)		# 再撮影
        vb2.addWidget(self.logButton)		# ログ
        vb2.addWidget(self.settingButton)	# 設定
        hb1.addLayout(vb2)		# /ボタン縦配置
        
        vb1.addLayout(hb1)	# /画像+ボタン
        
        vb1.addWidget( self.pbar )	# ゲージ
        
        self.setLayout(vb1)	# /全体
        
        # デバッグ用ウィンドウ
        self.debWindow = QWidget()
        self.videoLabel = QLabel(self.debWindow)	# ラベル
        self.videoLabel.setFixedSize(IMG_SIZE[0], IMG_SIZE[1])
        
        
    # 再撮影
    def on_clicked_recap(self):
        self.parent.setSheet(0)
    
    # ログ
    def on_clicked_log(self):
        self.parent.setSheet(2)
    
    # 設定
    def on_clicked_setting(self):
        print("setting")
        
    # 遷移時の処理(開始)
    def start(self):
        super().start()
        self.cvCap = cv2.VideoCapture(0)
        
        
    # 遷移時の処理(終了)
    def stop(self):
        super().stop()
        self.cvCap.release()
        self.cvCap = None
        
        self.debWindow.hide()
        
        
    # 描画イベント
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()			# キャプチャ
            frame2 = cv2.resize(self.frame1, IMG_SIZE )		# リサイズ
            frame2 = frame2[:,::-1]							# 左右反転
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)          # 画像貼り付け
            
            self.debWindow.show()
