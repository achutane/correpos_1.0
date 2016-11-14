#!/usr/bin/python
# -*- coding: utf-8 -*-

from sheet import sheet
import config

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# --- 定数 ---
BUTTON_SIZE = (200, 50)    # フォント23
BUTTON_START_POS = (400, 430)

IMG_SIZE = (1000, 500)
IMG1_POS = (100, 150)

TXT_START = "START"

# --- 初期画面 ---
class titleSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        # --- 画像配置 
        self.titleLabel = QLabel(self)
        self.pmap = QPixmap("title.png")
        self.titleLabel.setPixmap(self.pmap)
        self.titleLabel.setFixedSize(IMG_SIZE[0], IMG_SIZE[1])
        # self.titleLabel.move(IMG1_POS[0], IMG1_POS[1])    # 位置

        # Startボタン
        self.startButton = QPushButton(TXT_START, self)                    # 生成
        self.startButton.clicked.connect(self.on_clicked_start)            # クリック時
        self.startButton.setFixedSize(BUTTON_SIZE[0], BUTTON_SIZE[1] )                # サイズ
        self.startButton.move(BUTTON_START_POS[0], BUTTON_START_POS[1])    # 位置
        
        # 配置
        # self.move(32, 16)
        # vbox = QVBoxLayout()
        # vbox.setSpacing(16)
        # h1 = QHBoxLayout()
        # h1.setSpacing(32)
        # h1.addWidget( self.titleLabel, 0, Qt.AlignCenter )
        # vbox.addLayout(h1)
        # h1 = QHBoxLayout()
        # h1.setSpacing(32)
        # h1.addWidget( self.startButton, 0, Qt.AlignCenter )
        # vbox.addLayout(h1)
        # self.setLayout(vbox)
        
    # 動作開始
    def start(self):
        super().start()
        
    # 動作終了
    def stop(self):
        super().stop()
        
    # Nextボタンの動作
    def on_clicked_start(self):
        # 処理
        print("start")
        self.parent.setSheet(0)

