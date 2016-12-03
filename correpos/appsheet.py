#!/usr/bin/python
# -*- coding: utf-8 -*-

from sheet import sheet
import config

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import log
import datetime
import cv2
import wavplay_pygame
from os.path import join, relpath
from glob import glob
import copy
import pandas as pd
import os.path
import option

# --- 定数 ---
IMG_SIZE = (400, 300)

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# --- 動作中画面 ---
class appSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        
        #判定レベル、状態画像表示に関する変数初期化
        self.picturechange = 0
        self.count = 50
        self.multi = 2
        self.th = 35       #顔の距離の閾値
        self.multi_y = 0.3   #顔の上下の判定
        
        self.selectSE = "!.wav"	# デフォルトSE
        self.subwindow = None	# 設定ウィンドウ宣言(None)
        
        self.setUI()
        
    # UI設定
    def setUI(self):
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
        self.nekoze_pbar = QProgressBar()
        self.nekoze_pbar.setTextVisible(False)	# パーセント表示オフ
        self.nekoze_pbar.setFixedHeight(8)		# 高さ
        self.nekoze_pbar.setValue(30)			# 値設定(適当)
        
        
        # ログ枠
        self.text = QTextEdit(self)
        self.text.move(50,400)
        self.text.resize(400,150)
        
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
        
        vb1.addWidget( self.nekoze_pbar )	# ゲージ
        
        self.setLayout(vb1)	# /全体
        
        # デバッグ用ウィンドウ
        self.debWindow = QWidget()
        vb1 = QVBoxLayout()
        
        # ラベル
        self.videoLabel = QLabel()
        self.videoLabel.setFixedSize(IMG_SIZE[0], IMG_SIZE[1])
        vb1.addWidget(self.videoLabel)
        
        # ログ枠
        vb1.addWidget( self.text )
        self.debWindow.setLayout( vb1 )
        
        
    # 再撮影
    def on_clicked_recap(self):
        self.parent.setSheet(0)
    
    # ログ
    def on_clicked_log(self):
        print("log")
        log.LOG()
    
    # 設定
    def on_clicked_setting(self):
        print("setting")
        option.option(self)
        
        
    # 開始ログ
    def start_log(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S") 
        self.text.append(daystr+"  START!!!")
        
    # タイマー起動
    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        
    # タイムアウト処理
    def timeout(self):
        self.nekose_check()
        self.timer.setInterval(10)
        self.timer.start()
        self.checkWorkHour()
        self.repaint()
        
    # 猫背チェック
    def nekose_check(self):        
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        
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
        
        # 猫背チェック処理
        self.levelcheck()
        self.facelevelcheck()
        
        if(self.evalNekose(self.width, self.height, config.width_s, config.height_s)):    # 評価
            
            #ゲージ増加レベルに関する変数代入
            if(self.parent.bar_num == 0):
                self.count = 100   #カウント数
                self.multi = 1     #倍数
            elif(self.parent.bar_num == 1):
                self.count = 50
                self.multi = 2
            elif(self.parent.bar_num == 2):
                self.count = 25
                self.multi = 4
            
            #判定レベルに関する変数代入
            if(self.parent.judgelevel_num == 0):
                self.multi_y = 0.5   #顔の上下の判定
                self.th = 50           #顔の距離の閾値
            elif(self.parent.judgelevel_num == 1):
                self.multi_y = 0.3
                self.th = 35
            elif(self.parent.judgelevel_num == 2):
                self.multi_y = 0.2
                self.th = 35
            
            if self.face: # 顔が認識されている場合
                self.check = (self.check + 1)%(self.count + 1)    # カウント
                
            self.nekoze_pbar.setValue(self.check*self.multi) #checkを猫背ゲージに代入
            if self.check == self.count: # 指定回カウント後
#                self.pmap = QPixmap("nekoze.png")
#                self.noticeLabel.setPixmap(self.pmap)
#                self.picturechange = 0
                self.notice()       # 通知
                self.time_draw()    # ログ追加
                self.check = 0
                self.nekoze_pbar.setValue(self.check * self.multi)
                
        else:
            if self.check > 0:            
                self.check = self.check - 1
                self.nekoze_pbar.setValue(self.check*self.multi) #checkを猫背ゲージに代入

    # 猫背時刻出力
    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")        
        self.text.append(daystr+"猫背を検知！")      
        self.add_log()

    # ログ保存
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
        
        
    # 通知処理
    def notice(self):
        if(self.parent.notice_num == 1 ): # 通知をする場合
            wavplay_pygame.play(self.selectSE, self.parent.volume_num) #選択したSEを鳴らす
            # その他通知(あれば)
            if(self.parent.popup_num == 1 ): # 通知をする場合
                self.balloon()
    
    # 判定レベル設定
    def levelcheck(self):
        pass
    
    # 
    def facelevelcheck(self):
        pass
        
    
    # 猫背評価
    def evalNekose(self, w1, h1, w0, h0):
        
        s1 = w1 * h1	# 現在の面積
        s0 = w0 * h0	# 基準の面積
        #th = 35			# 閾値
        
        # 評価
        ev = abs( (s1 - s0) / s0 * 100 )
        
        # 出力
        #print(ev)
        
        # 判定
        if self.face==False:
#                self.nekozecondition_settext.setText("顔みつからない")
                return 1
        elif ev >self.th: #顔の距離
            if s1-s0>0:
#                self.nekozecondition_settext.setText("画面に近い")
                return 1
            else:
#                self.nekozecondition_settext.setText("画面から遠い")
                return 0
        elif self.face_y>config.face_y+config.height_s*self.multi_y: #顔のｙ座標（たて）のチェック 顔の高さの0.3倍で検知
#            self.nekozecondition_settext.setText("顔が下がってる")
            return 1
        else:
#            self.nekozecondition_settext.setText("背筋ピーン")
            return 0
        #return ev > th
    
    # バルーン表示
    def balloon(self):
        icon = QSystemTrayIcon.MessageIcon(2) # 引数によりアイコンが変わる
        config.trayIcon.showMessage("CorrePos","猫背検知！！", icon, 5000) # 最後の引数は自動消失までの時間(ms)．
        # 参考URL http://kyoui3350.blog96.fc2.com/blog-entry-344.html
        # http://pyqt.sourceforge.net/Docs/PyQt4/qsystemtrayicon.html
        
            
    # 作業終了時刻
    def checkWorkHour(self):
        # 設定が有効
        if(self.parent.work_num == 1 ):
          currentTime = QDateTime.currentDateTime().time().toString("hh:mm")
          self.parent.worktime = self.workHourEdit.time().toString("hh:mm")
          
          # 終了時刻になった
          if(currentTime == self.parent.worktime):
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
              self.parent.work_num = 0
              self.parent.notice_num = 0
              
              self.write_log(str)

    # -------- オプション関係 --------
    def selectSE_onActivated(self,text):
        self.selectSE=text #selectSEにファイル名を代入
        self.selectSE_name=text
        #self.selectSE_list=self.SElist.index
        wavplay_pygame.play(text,self.parent.volume_num) #音を鳴ら
        
    
    def text_draw(self): #音量設定のVolumeが変更されたときに表示テキストを変える
        self.slider_label.setText('音量 :'+str(self.parent.volume_num))
        self.parent.volume_num=self.slider.value()
        
        
    def button_clicked(self): #音量テストのボタンが押されたときに走る
        button = self.sender()
        if button is None or not isinstance(button,QPushButton):
            return
        wavplay_pygame.play(self.selectSE,self.parent.volume_num)
        
        
    def on_clicked_noticeEnable(self): #optionの通知を押したときの処理
        self.parent.notice_num =  (self.parent.notice_num+1)%2
        
    def on_clicked_message_boxEnable(self): #optionのポップアップ通知を押したときの処理
        self.parent.popup_num =  (self.parent.popup_num+1)%2
        #print(self.parent.popup_num)
        
    def on_clicked_workHourEdit(self): #optionの作業時間の通知ＯＮ・ＯＦＦの処理
        self.parent.work_num =  (self.parent.work_num+1)%2
        #print(self.parent.popup_num)
        
        
    #判定レベルのラジオボタンを押したときの処理
    def on_clicked_clevel1(self):
        self.parent.judgelevel_num = 0
    def on_clicked_clevel2(self):
        self.parent.judgelevel_num = 1
    def on_clicked_clevel3(self):
        self.parent.judgelevel_num = 2 

    #ゲージ増加レベルのラジオボタンを押したときの処理
    def on_clicked_level1(self):
        self.parent.bar_num = 0
    def on_clicked_level2(self):
        self.parent.bar_num = 1
    def on_clicked_level3(self):
        self.parent.bar_num = 2 


    # -------- シート/ウィンドウ処理 --------
    # 遷移時の処理(開始)
    def start(self):
        super().start()
        self.start_log()
        self.auto()
        self.cvCap = self.parent.cvCap
        self.check = 1
        self.face = False	# 顔が認識されている場合True
        
        
    # 遷移時の処理(終了)
    def stop(self):
        super().stop()
        
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

    #
    def closeEvent(self, event):
        if not self.subwindow is None:
            self.subwindow.close()
        self.debWindow.close()