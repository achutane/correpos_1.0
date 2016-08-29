#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import datetime
import cv2
import windowframe


# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = windowframe.myWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()