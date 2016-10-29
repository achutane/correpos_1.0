#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --- シートテンプレ ---
class sheet(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resize(0,0)
        
    def start(self):
        # 有効化
        self.adjustSize()	# サイズ復元
        self.setVisible(True)
        
    def stop(self):
        # 無効化
        self.resize(0,0)	# 最小化
        self.setVisible(False)
