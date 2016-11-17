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
        self.recapButton = QPushButton( QIcon("cameraIcon.png"), "")
        self.logButton = QPushButton( QIcon("logIcon.png"), "")
        self.settingButton = QPushButton( QIcon("settingIcon.png"), "")
        
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
        
    def start(self):
        super().start()
        
          
    def stop(self):
        super().stop()
