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
import tkinter # ポップアップ表示に必要
import tkinter.messagebox as tkmsg # ポップアップ表示に必要
from os.path import join, relpath
from glob import glob

# --- 定数 ---
IMG_SIZE = (400, 300)

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# --- 動作中画面 ---
class driveSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.text = QTextEdit(self)		# ログ枠
        self.text.move(50,400)
        self.text.resize(400,150)
        self.videoLabel = QLabel(self)	# 映像表示
        self.videoLabel.resize(400,300)        
        self.videoLabel.move(50,50)
        self.noticeEnable = QCheckBox(self)	# 通知オン・オフ
        self.noticeEnable.move(700, 50)
        self.noticeEnable.setText("通知する")
        self.noticeEnable.setTristate(False)
        
        self.descLabel = QLabel(self)
        self.descLabel.move(650, 78)
        #self.descLabel.resize(50, 30)
        self.descLabel.setText("通知音設定 ： ")
        self.combo_selectSE = QComboBox(self) #SEを変えるComboBoxの作成
        self.combo_selectSE.move(750,75) #ComboBoxの座標指定
        path='wav_SE'
        list = [relpath(x, path) for x in glob(join(path, '*.wav'))] #wav_SEのファイル名を抽出
        for file in list:
            self.combo_selectSE.addItem(file)
        self.selectSE=list[0] #select_SEに文字列を代入　後でwavplayで使用
        self.combo_selectSE.activated[str].connect(self.selectSE_onActivated) #ComboBoxで選んだ時の動作
           
        self.w=QWidget(self) #音量設定の枠wの作成
        self.w.setGeometry(650,100,300,100) #音量設定の枠の座標 (y,x,width,height)     
        self.slider = QSlider(Qt.Vertical)  #スライダの向き
        self.slider.setRange(0, 100)  # スライダの範囲
        self.slider.setValue(50)  # 初期値
        self.slider_label = QLabel('Volume :'+str(self.slider.value())) #volume:スライダの値
        self.slider.valueChanged.connect(self.text_draw) #スライダの値が変わったらtext_drawを実行                
        self.checkbutton = QPushButton("音量テスト") #音量の確認ボタン
        self.checkbutton.setFocusPolicy(Qt.NoFocus)
        self.checkbutton.clicked.connect(self.button_clicked) #音量テストのボタンを押すとbutton_clicked実行
        
        self.changevolume=QHBoxLayout(self) #音量テストをまとめる横方向のレイアウトの作成
        self.changevolume.addWidget(self.slider_label)
        self.changevolume.addWidget(self.slider)
        self.changevolume.addWidget(self.checkbutton)        
        self.w.setLayout(self.changevolume) #レイアウトをｗに突っ込む

        # deb:再設定
        self.b = QPushButton("再設定", self)
        self.b.clicked.connect(self.on_clicked)
        
    def on_clicked(self):
        print("clicked @ sheet2")
        self.parent.setSheet(0)
  
    def start(self):
        super().start()
        self.auto()
        self.cvCap = cv2.VideoCapture(0)
        self.check = 1
        
        self.noticeEnable.setChecked(True)


          
    def stop(self):
        super().stop()
        # カメラリリース
        self.cvCap.release()
        self.cvCap = None
        
        # タイマー終了
        self.timer.stop()
        
        
    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")        
        self.text.append(daystr+"猫背を検知！")      
        
        #タイマーの起動
    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
           
           #タイムアウト処理
    def timeout(self):
        self.nekose_check()
        self.timer.setInterval(10)
        self.timer.start()
        
        #猫背をチェックする
    def nekose_check(self):
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        print(facerect)
        
        if(len(facerect) > 0):	# 顔検出した 
            # サイズ取り出し
            # 顔選択:とりあえず面積最大
            w0 = facerect[0][2]    # 幅
            h0 = facerect[0][3]    # 高さ
            s0 = w0 * h0
            for i in range(1, len(facerect)):   # すべての顔について
                w1 = facerect[i][2]
                h1 = facerect[i][3]
                s1 = w1 * h1
                if(s0 < s1):    # 面積が大きい
                    w0 = w1     # 更新
                    h0 = h1
                    s0 = s1
            # サイズ確定
            self.width = w0
            self.height = h0
        
        # 猫背チェック
#        if self.width >= width_s*1.5 and self.height >= height_s*1.5:

        if(self.evalNekose(self.width, self.height, config.width_s, config.height_s)):    # 評価
            self.check = (self.check + 1)%50    # カウント
            print(self.check)
            if self.check == 0: # 50カウント後
                self.notice()       # 通知
                self.time_draw()    # ログ追加
                
        else:
            if self.check > 0:            
                self.check = self.check - 1

    # 通知を行う
    def notice(self):
        if(self.noticeEnable.isChecked() ): # 通知をする場合
            sound = "dog01"
            if(self.soundselect1.isChecked()):
                sound="dog01"
            elif(self.soundselect2.isChecked()):
                sound="bird05"
            elif(self.soundselect3.isChecked()):
                sound="tiger01"
            
            elif(self.soundselect4.isChecked()):
                sound="nc131523"
                
            wavplay_pygame.play(sound,self.slider.value())
            # その他通知(あれば)
            self.message_box()
    
    # 猫背評価
    def evalNekose(self, w1, h1, w0, h0):

        s1 = w1 * h1	# 現在の面積
        s0 = w0 * h0	# 基準の面積
        th = 35			# 閾値
        
        # 評価
        ev = abs( (s1 - s0) / s0 * 100 )
        
        # 出力
        print(ev)
        
        # 判定
        return ev > th
        
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()    # キャプチャ
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # リサイズ
            frame2 = frame2[:,::-1]                    # 左右反転
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け

            
    def text_draw(self): #音量設定のVolumeが変更されたときに表示テキストを変える
        self.slider_label.setText('Volume :'+str(self.slider.value()))
        
    def button_clicked(self): #音量テストのボタンが押されたときに走る
        button = self.sender()
        if button is None or not isinstance(button,QPushButton):
            return
        wavplay_pygame.play(self.selectSE,self.slider.value())
    
    def message_box(self): # ポップアップ表示
        root = tkinter.Tk()
        root.withdraw() # <- これでTkの小さいウィンドウが非常時になる
        tkmsg.showwarning('correpos', '猫背検知！！')
        # 参考URL http://ameblo.jp/hitochan007/entry-12028166427.html
        
    def selectSE_onActivated(self,text):
        self.selectSE=text #selectSEにファイル名を代入
        wavplay_pygame.play(text,self.slider.value()) #音を鳴ら