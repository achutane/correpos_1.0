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
class driveSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.text = QTextEdit(self)		# ログ枠
        self.text.move(50,400)
        self.text.resize(400,150)
        self.videoLabel = QLabel(self)	# 映像表示
        self.videoLabel.resize(400,300)        
        self.videoLabel.move(50,50)
        self.nekozegauge_text=QLabel(self) #猫背ゲージの作成
        self.nekozegauge_text.setText("猫背ゲージ　")
        self.nekozegauge_text.setGeometry(50,360,70,30)
        self.nekoze_pbar = QProgressBar(self)  #ゲージ本体
        self.nekoze_pbar.setGeometry(120,370,200,10)
        self.nekozecondition_text=QLabel(self) #猫背状態の通知
        self.nekozecondition_text.setText("状態：")
        self.nekozecondition_text.setGeometry(345,360,70,30)
        self.nekozecondition_settext=QLabel(self) #猫背状態の通知
        self.nekozecondition_settext.setText("背筋ピーン")
        self.nekozecondition_settext.setGeometry(375,360,70,30)
        
        
        self.noticeEnable = QCheckBox(self)	# 通知オン・オフ
        self.noticeEnable.move(700, 50)
        self.noticeEnable.setText("通知する")
        self.noticeEnable.setTristate(False)
        self.message_boxEnable = QCheckBox(self)	# ポップアップ通知オン・オフ
        self.message_boxEnable.move(800, 50)
        self.message_boxEnable.setText("ポップアップ通知")
        self.message_boxEnable.setTristate(False)
        
        #判定厳しさ調整のラジオボタン作成
        self.sldlevel = QLabel(self)
        self.sldlevel.move(610,240)
        self.sldlevel.setText("ゲージ増加レベル:")
        self.level1=QRadioButton("すこし", self)    #判定レベル　ラジオボタン作成
        self.level1.move(750,240)
        self.level2=QRadioButton("ふつう", self)
        self.level2.move(800,240)
        self.level3=QRadioButton("おおい", self)
        self.level3.move(850,240)
        self.levelgroup=QButtonGroup(self)    #ラジオボタン　グループ作成
        self.levelgroup.addButton(self.level1)
        self.levelgroup.addButton(self.level2)
        self.levelgroup.addButton(self.level3)
        self.leveltext = QLabel(self)
        self.leveltext.resize(50,30)
        self.leveltext.move(700,233)
        self.leveltext.setText("ふつう")
        
        self.descLabel = QLabel(self)
        self.descLabel.move(650, 78)
        #self.descLabel.resize(50, 30)
        self.descLabel.setText("通知音設定 ： ")
        self.combo_selectSE = QComboBox(self) #ComboBoxの作成
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

 #通知画像表示
        self.noticeLabel = QLabel(self)
        self.noticeLabel.move(700,250)
        self.pmap = QPixmap("man.png")
        self.noticeLabel.setPixmap(self.pmap)
        
        #判定レベル、状態画像表示に関する変数初期化
        self.picturechange = 0
        self.level = 2
        self.count = 50
        self.multi = 2
        
        # 作業終了時刻の設定
        self.workHourButton = QCheckBox(self)                      # 有効・無効設定
        self.workHourButton.setText("作業終了時刻を設定する：")
        self.workHourButton.move(650, 200)
        self.workHourButton.setTristate(False)
        self.workHourEdit = QDateTimeEdit(self)                    # 時刻設定
        self.workHourEdit.move(800, 200)
        self.workHourEdit.setDisplayFormat("hh:mm")

        # deb:再設定
        self.b = QPushButton("再設定", self)
        self.b.clicked.connect(self.on_clicked)

        # バルーンのためのアイコン（右下に常駐）
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("man.png")) # とりあえず適当にこの画像
        self.trayIcon.show()

        self.logbutton = QPushButton("log",self)
        self.logbutton.clicked.connect(self.on_clicked_log)
        self.logbutton.move(50,550)
        
    def on_clicked_log(self):
        self.parent.setSheet(2)
        
    def on_clicked(self):
        print("clicked @ sheet2")
        self.parent.setSheet(0)
  
    def start(self):
        super().start()
        self.auto()
        self.cvCap = cv2.VideoCapture(0)
        self.check = 1
        self.face = False   #顔が認識されている場合True
        
        self.noticeEnable.setChecked(True)
        self.message_boxEnable.setChecked(True)


          
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
        self.add_log()

    def add_log(self):
        if os.path.exists("log.csv"):
            df = pd.read_csv('log.csv')
            df = df['0']
            df = df.append(pd.DataFrame([datetime.datetime.today()]))
            
        else:
            df = pd.DataFrame([datetime.datetime.today()])

        df.to_csv('log.csv')
    # time_drawを汎用化した
    def write_log(self, log):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")        
        self.text.append(daystr+log) 
        
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
        self.checkWorkHour()
        
        #猫背をチェックする
    def nekose_check(self):
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        print(facerect)
        
        if(len(facerect) > 0):	# 顔検出した
            self.face = True 
            # サイズ取り出し
            # 顔選択:とりあえず面積最大
            x0=facerect[0][0]
            y0=facerect[0][1]
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
                    x0=facerect[i][0]
                    y0=facerect[i][1]
            # サイズ確定
            self.width = w0
            self.height = h0
            self.face_x=x0
            self.face_y=y0

        else:
            self.face =False

        
        # 猫背チェック
#        if self.width >= width_s*1.5 and self.height >= height_s*1.5:
        self.levelcheck()
        if(self.evalNekose(self.width, self.height, config.width_s, config.height_s)):    # 評価
            
            #判定レベルに関する変数代入
            if(self.level == 1):
                self.count = 100
                self.multi = 1
            elif(self.level == 2):
                self.count = 50
                self.multi = 2
            elif(self.level == 3):
                self.count = 25
                self.multi = 4
            
            
            #一定時間で元の姿勢画像に戻す
            self.picturechange = self.picturechange + 1
            if self.picturechange == 10:
                print("change!!")
                self.pmap = QPixmap("man.png")
                self.noticeLabel.setPixmap(self.pmap)
            if self.face: # 顔が認識されている場合
                self.check = (self.check + 1)%(self.count + 1)    # カウント
            self.nekoze_pbar.setValue(self.check*self.multi) #checkを猫背ゲージに代入
            if self.check == self.count: # 50カウント後
                self.pmap = QPixmap("nekoze.png")
                self.noticeLabel.setPixmap(self.pmap)
                self.picturechange = 0
                self.notice()       # 通知
                self.time_draw()    # ログ追加
                self.check = 0
                self.nekoze_pbar.setValue(self.check * self.multi)
                
        else:
            if self.check > 0:            
                self.check = self.check - 1
                self.nekoze_pbar.setValue(self.check*self.multi) #checkを猫背ゲージに代入

    def notice(self):
        if(self.noticeEnable.isChecked() ): # 通知をする場合
            wavplay_pygame.play(self.selectSE,self.slider.value()) #選択したSEを鳴らす
            # その他通知(あれば)
            if(self.message_boxEnable.isChecked() ): # 通知をする場合
                self.balloon()
    
    #判定レベル設定
    def levelcheck(self):
        if(self.noticeEnable.isChecked() ):
            self.level = 2
            if(self.level1.isChecked()):
                self.leveltext.setText("すこし")
                self.level = 1
            elif(self.level2.isChecked()):
                self.leveltext.setText("ふつう")
                self.level = 2
            elif(self.level3.isChecked()):
                self.leveltext.setText("おおい")
                self.level = 3
    
    
    # 猫背評価
    def evalNekose(self, w1, h1, w0, h0):
        
        

        s1 = w1 * h1	# 現在の面積
        s0 = w0 * h0	# 基準の面積
        th = 35			# 閾値
        
        # 評価
        ev = abs( (s1 - s0) / s0 * 100 )
        
        # 出力
        #print(ev)
        
        # 判定
        if ev >th: #顔の距離
            if s1-s0>0:
                self.nekozecondition_settext.setText("画面に近い")
                return 1
            else:
                self.nekozecondition_settext.setText("画面から遠い")
                return 0
        elif self.face_y>config.face_y+config.height_s*0.3: #顔のｙ座標（たて）のチェック 顔の高さの0.3倍で検知
            self.nekozecondition_settext.setText("顔が下がってる")
            return 1
        else:
            self.nekozecondition_settext.setText("背筋ピーン")
            return 0
        #return ev > th
        
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

    def message_box(self): # ポップアップ表示 message  使わないけど一応残しとくmessage
        QMessageBox.warning(self, "CorrePos", u"猫背検知！！")
        self.show()
        # 参考URL http://myenigma.hatenablog.com/entry/2016/01/24/113413#メッセージボックスを作る

    def balloon(self): # バルーン表示
        icon = QSystemTrayIcon.MessageIcon(2) # 引数によりアイコンが変わる
        self.trayIcon.showMessage("CorrePos","猫背検知！！", icon, 5000) # 最後の引数は自動消失までの時間(ms)．
        # 参考URL http://kyoui3350.blog96.fc2.com/blog-entry-344.html
        # http://pyqt.sourceforge.net/Docs/PyQt4/qsystemtrayicon.html

    def selectSE_onActivated(self,text):
        self.selectSE=text #selectSEにファイル名を代入
        wavplay_pygame.play(text,self.slider.value()) #音を鳴ら
        
    # 作業終了時刻
    def checkWorkHour(self):
        # 設定が有効
        if(self.workHourButton.isChecked() ):
          currentTime = QDateTime.currentDateTime().time().toString("hh:mm")
          workTime = self.workHourEdit.time().toString("hh:mm")
          
          # 終了時刻になった
          if(currentTime == workTime):
              str = "作業終了！"
              print(str)
              
              # 終了通知
              self.dlg = QMessageBox(self)
              self.dlg.setText(str)
              self.dlg.setWindowTitle("CorrePos")
              self.dlg.show()
              self.activateWindow()
              
              self.workHourButton.setChecked(False)
              self.noticeEnable.setChecked(False)    # 通知を無効化（暫定）

              self.write_log(str)
