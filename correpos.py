#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import datetime
import cv2




# --- 定数 ---

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_SIZE = (1200, 600)

BUTTON_SIZE = (100, 23)    # フォント23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_CAP = "撮影"
TXT_RECAP = "再撮影"

TXT_NEXT = "次へ"

width_s = 0
height_s = 0

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# --- シートテンプレ ---
class sheet(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resize(0,0)
        
    def start(self):
        # 有効化
        self.resize(self.parent.width(), self.parent.height() )
        self.setVisible(True)
        
    def stop(self):
        # 無効化
        self.resize(0,0)
        self.setVisible(False)



# --- 初期画面 ---
class initSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        # --- ボタン配置 ---
        # 撮影ボタン
        self.capButton = QPushButton(TXT_CAP, self)                    # 生成、キャプション
        self.capButton.clicked.connect(self.on_clicked_cap)            # クリック時の動作
        self.capButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )        # サイズ設定
        self.capButton.move(BUTTON_CAP_POS[0], BUTTON_CAP_POS[1])    # 位置
        
        # Nextボタン
        self.nextButton = QPushButton(TXT_NEXT, self)                    # 生成
        self.nextButton.clicked.connect(self.on_clicked_next)            # クリック時
        self.nextButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )                # サイズ
        self.nextButton.move(BUTTON_NEXT_POS[0], BUTTON_NEXT_POS[1])    # 配置
        self.nextButton.setEnabled(False)                                # 無効化

        
        # --- 画像配置 ---
        # 映像表示
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
        self.videoLabel.move(IMG1_POS[0], IMG1_POS[1])
        
        # スクショ表示
        self.capLabel = QLabel(self)
        self.capLabel.move(IMG2_POS[0], IMG2_POS[1])
        self.capLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
        
        self.cvCap = None
        
    # 動作開始
    def start(self):
        super().start()
        
        # カメラ使用
        self.cvCap = cv2.VideoCapture(0)
        
        # ボタン初期化
        self.capButton.setText(TXT_CAP)        # 撮影ボタン
        self.nextButton.setEnabled(False)    # 次へボタン
        
    # 動作終了
    def stop(self):
        super().stop()
        
        # カメラリリース
        self.cvCap.release()
        self.cvCap = None
        
        # 画像廃棄
        self.capLabel.setPixmap(QPixmap())
    
    
    # 撮影ボタンの動作
    def on_clicked_cap(self):
        self.capButton.setText(TXT_RECAP)    # テキスト変更
        self.nextButton.setEnabled(True)    # ToDo "次へ"ボタン有効化
        
        
        color = (255, 255, 255) #白
        #物体認識（顔認識）の実行
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        #座標取得
        for rec in facerect:
            width_s = rec[2]
            height_s = rec[3]
  
        
        # カメラ映像キャプチャ
        img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.capLabel.setPixmap(pix)
        
        
    # Nextボタンの動作
    def on_clicked_next(self):
        # 処理
        print("next")
        self.parent.setSheet(1)

    """
    def on_clicked(self):
        print("clicked @ sheet1")
        self.parent.setSheet(1)
    """
    
    # 再描画イベント：タイマーにしたい
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()    # キャプチャ
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # リサイズ
            frame2 = frame2[:,::-1]                    # 左右反転
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け





# --- 動作中画面 ---
class driveSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.b = QPushButton("test2", self)
        self.b.clicked.connect(self.on_clicked)
        self.text = QTextEdit(self)
        self.text.move(10,10)
        self.text.resize(140,140)
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(400,300)        
        self.videoLabel.move(500,100)
        
    def on_clicked(self):
        print("clicked @ sheet2")
        self.parent.setSheet(0)
  
    def start(self):
        super().start()
        self.auto()
        self.cvCap = cv2.VideoCapture(0)
        self.check = 0


          
    def stop(self):
        super().stop()
        # カメラリリース
        self.cvCap.release()
        self.cvCap = None
        
        
    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")
        #self.text.append(daystr)        
        
    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
           
    def timeout(self):
        print ("hoge")
        self.nekose_check()
        self.time_draw()
        self.timer.setInterval(10)
        self.timer.start()
        
    def nekose_check(self):
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        #座標取得
        for rec in facerect:
            self.width = rec[2]
            self.height = rec[3]    
        
        if self.width >= width_s*1.5 and self.height >= height_s*1.5:
            self.check = self.check + 1
            print(self.check)

    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()    # キャプチャ
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # リサイズ
            frame2 = frame2[:,::-1]                    # 左右反転
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け





# --- ウィンドウ ---
class myWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ウィンドウ設定
        self.setWindowTitle(APPNAME)                        # キャプション
#        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])    # サイズ
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        # シート作成
        self.sheets = []
        self.sheets.append(initSheet(self) )
        self.sheets.append(driveSheet(self) )
        
        self.current = 0
        self.sheets[self.current].start()
        
        # ウィンドウ表示
        self.show()
        
    # シート切り替え
    def setSheet(self, num):
        self.sheets[self.current].stop()
        self.current = num
        self.sheets[self.current].start()
            





# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = myWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()