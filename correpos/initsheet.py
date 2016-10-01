#!/usr/bin/python
# -*- coding: utf-8 -*-

from sheet import sheet
import config

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2
import copy

# --- 定数 ---
BUTTON_SIZE = (100, 23)    # フォント23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_DESC1 = "正しい姿勢で座り、[撮影]を押します"
TXT_DESC2 = "再度撮影する場合は[撮影]、猫背検知を開始するには[次へ]を押します"

TXT_CAP = "撮影"
TXT_RECAP = "再撮影"

TXT_NEXT = "次へ"


cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 


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

        # --- ラベル配置 ---
        self.descLabel = QLabel(self)
        self.descLabel.move(100, 50)
        self.descLabel.resize(1100, 30)
        
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
        
        # ラベル
        self.descLabel.setText(TXT_DESC1)
        
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
        # 顔のサイズ取得
        # global width_s,height_s
        color = (255, 255, 255) # 白
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))	# 顔認識
        
        print(facerect) # 認識結果出力
        
        if(len(facerect) > 0):	# 顔検出した
            # サイズ取り出し
            # 顔選択:とりあえず面積最大
            w0 = facerect[0][2]    # 幅
            h0 = facerect[0][3]    # 高さ
            s0 = w0 * h0
            for i in range(len(facerect)):   # すべての顔について
                w1 = facerect[i][2]
                h1 = facerect[i][3]
                s1 = w1 * h1
                if(s0 < s1):    # 面積が大きい
                    w0 = w1     # 更新
                    h0 = h1
                    s0 = s1
            # サイズ確定
            config.width_s = w0
            config.height_s = h0
            print((config.width_s, config.height_s))	# サイズ出力
            
        	# テキスト変更
            self.capButton.setText(TXT_RECAP)    # テキスト変更
            self.descLabel.setText(TXT_DESC2)
            
            # [次へ]有効化
            self.nextButton.setEnabled(True)            
            
        else:	# 顔検出せず
            self.capButton.setText(TXT_CAP)   # テキスト変更
            self.descLabel.setText(TXT_DESC3)	# エラーメッセージ
            self.nextButton.setEnabled(False)	# [次へ]無効
        
        # カメラ映像キャプチャ
        # 撮影画像表示
        frame2 = cv2.resize(self.frame1, IMG_SIZE )		# リサイズ
        frame2 = frame2[:,::-1]							# 左右反転
        frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
        img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.capLabel.setPixmap(pix)	# 画像貼り付け
            
        
    # Nextボタンの動作
    def on_clicked_next(self):
        # 処理
        print("next")
        self.parent.setSheet(1)
    
    # 再描画イベント：タイマーにしたい
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()			# キャプチャ
            frame = copy.deepcopy(self.frame1)				# フレームのコピー
            
            #物体認識（顔認識）の実行
            facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

            color = (255, 255, 255) # 白
            for rect in facerect:
                #検出した顔を囲む矩形の作成
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)

            
            frame2 = cv2.resize(frame, IMG_SIZE )		# リサイズ
            frame2 = frame2[:,::-1]							# 左右反転
            
            frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け

