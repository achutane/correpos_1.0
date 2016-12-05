#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton) 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from glob import glob
from os.path import join, relpath




def option(self):
    
    self.subwindow = QWidget()
    self.subwindow.setWindowTitle("OPTION")
    self.subwindow.setWindowIcon(QIcon('img/correpos_icon.png')) #iconをそろえた
    
    """
    #背景をmainのシートと合わせようとしたが文字が見にくいので良いのがあれば後で編集
    color = QColor(100,100,100,100)
    color.setAlpha(150)
    palette = QPalette()
    backgroundImage = QPixmap("img/backgroundImage.jpg")
    brash = QBrush(color, backgroundImage)
    palette.setBrush(palette.Background, brash)
    self.subwindow.setPalette(palette)
    """
    

    self.noticeEnable = QCheckBox()	# 通知オン・オフ
    self.noticeEnable.setText("通知する")
    self.noticeEnable.setTristate(False)
    if(self.parent.notice_num==1): #通知ＯＮかＯＦＦかを調べる
        self.noticeEnable.setChecked(True)
    else:
        self.noticeEnable.setChecked(False)
    self.message_boxEnable = QCheckBox()	# ポップアップ通知オン・オフ
    self.message_boxEnable.setText("バルーン通知")
    if(self.parent.popup_num==1): #バルーン通知ＯＮかＯＦＦかを調べる
        self.message_boxEnable.setChecked(True)
    else:
        self.message_boxEnable.setChecked(False)  
    # 作業終了時刻の設定
    self.workHourButton = QCheckBox()                      # 有効・無効設定
    self.workHourButton.setText("作業終了通知：")
    if(self.parent.work_num==1): #作業終了通知ＯＮかＯＦＦかを調べる
        self.workHourButton.setChecked(True)
    else:
        self.workHourButton.setChecked(False)
    self.workHourEdit = QDateTimeEdit()                    # 時刻設定
    self.workHourEdit.setDisplayFormat("hh:mm")
    self.grid_message=QGridLayout() #グリッド作成
    self.grid_message.addWidget(self.noticeEnable, 0, 0)
    self.grid_message.addWidget(self.message_boxEnable, 1, 0)
    self.grid_message.addWidget(self.workHourButton, 2, 0)
    self.grid_message.addWidget(self.workHourEdit, 2, 1)
    self.message_Widget=QWidget(self)
    self.message_Widget.setLayout(self.grid_message) 
    
    #通知音設定
    self.descLabel = QLabel()
    self.descLabel.setText("通知音設定 ： ")
    self.combo_selectSE = QComboBox() #ComboBoxの作成
    path='wav_SE'
    self.combo_selectSE.addItem(self.selectSE) #最初に選択中のＳＥを持ってきた
    list = [relpath(x, path) for x in glob(join(path, '*.wav'))] #wav_SEのファイル名を抽出
    for file in list:
        self.combo_selectSE.addItem(file)
    self.combo_selectSE.activated[str].connect(self.selectSE_onActivated) #ComboBoxで選んだ時の動作
    self.selectSE_frame=QHBoxLayout()
    self.selectSE_frame.addWidget(self.descLabel)
    self.selectSE_frame.addWidget(self.combo_selectSE)
    self.selectSE_widget=QWidget()
    self.selectSE_widget.setLayout(self.selectSE_frame) #レイアウトをｗに突っ込む    
        
    self.slider = QSlider(Qt.Horizontal)  #スライダの向き
    self.slider.setRange(0, 100)  # スライダの範囲
    self.slider.setValue(self.parent.volume_num)  # 初期値
    self.slider_label = QLabel('音量 :'+str(self.slider.value())) #volume:スライダの値
    self.slider.valueChanged.connect(self.text_draw) #スライダの値が変わったらtext_drawを実行                
    self.checkbutton = QPushButton("音量テスト") #音量の確認ボタン
    self.checkbutton.setFocusPolicy(Qt.NoFocus)
    self.checkbutton.clicked.connect(self.button_clicked) #音量テストのボタンを押すとbutton_clicked実行        
    self.changevolume=QHBoxLayout() #音量テストをまとめる横方向のレイアウトの作成
    self.changevolume.addWidget(self.slider_label)
    self.changevolume.addWidget(self.slider)
    self.changevolume.addWidget(self.checkbutton)
    self.volume_widget=QWidget() #音量設定の枠volume_widgetの作成
    self.volume_widget.setLayout(self.changevolume) #レイアウトをvolume_widgetに突っ込む
                
    #判定厳しさ調整のラジオボタン作成
    self.checklevel = QLabel()
    self.checklevel.setText("判定レベル:")
    self.levelyurui = QLabel()
    self.levelyurui.setText("緩")
    self.clevel1=QRadioButton("", self)    #判定レベル　ラジオボタン作成
    self.clevel2=QRadioButton("", self)
    self.clevel3=QRadioButton("", self)
    self.levelgen = QLabel()
    self.levelgen.setText("厳")
    self.clevelgroup=QButtonGroup()    #ラジオボタン　グループ作成
    self.clevelgroup.addButton(self.clevel1)
    self.clevelgroup.addButton(self.clevel2)
    self.clevelgroup.addButton(self.clevel3)
    self.clevelbuttom_frame=QHBoxLayout()
    self.clevelbuttom_frame.addWidget(self.levelyurui)
    self.clevelbuttom_frame.addWidget(self.clevel1)
    self.clevelbuttom_frame.addWidget(self.clevel2)
    self.clevelbuttom_frame.addWidget(self.clevel3)
    self.clevelbuttom_frame.addWidget(self.levelgen)
    self.clevelgroup_widget=QWidget()
    self.clevelgroup_widget.setLayout(self.clevelbuttom_frame) #レイアウトをvolume_widgetに突っ込む
    self.checklevel_frame=QHBoxLayout() #音量テストをまとめる横方向のレイアウトの作成
    self.checklevel_frame.addWidget(self.checklevel)
    self.checklevel_frame.addWidget(self.clevelgroup_widget)
    self.checklevel_widget=QWidget()
    self.checklevel_widget.setLayout(self.checklevel_frame) 
    if(self.parent.judgelevel_num == 0): #いま選択している所をチェック
        self.clevel1.setChecked(True)
    elif(self.parent.judgelevel_num == 1):
        self.clevel2.setChecked(True)
    else:
        self.clevel3.setChecked(True)
    
    #ゲージ増加調整のラジオボタン作成
    self.sldlevel = QLabel()
    self.sldlevel.setText("ゲージ増加レベル:")
    self.levelslow = QLabel()
    self.levelslow.setText("遅")
    self.level1=QRadioButton("", self)    #判定レベル　ラジオボタン作成
    self.level2=QRadioButton("", self)
    self.level3=QRadioButton("", self)
    self.levelquick = QLabel()
    self.levelquick.setText("早")
    self.levelgroup=QButtonGroup()    #ラジオボタン　グループ作成
    self.levelgroup.addButton(self.level1)
    self.levelgroup.addButton(self.level2)
    self.levelgroup.addButton(self.level3)
    self.levelbuttom_frame=QHBoxLayout()
    self.levelbuttom_frame.addWidget(self.levelslow)
    self.levelbuttom_frame.addWidget(self.level1)
    self.levelbuttom_frame.addWidget(self.level2)
    self.levelbuttom_frame.addWidget(self.level3)
    self.levelbuttom_frame.addWidget(self.levelquick)
    self.levelgroup_widget=QWidget()
    self.levelgroup_widget.setLayout(self.levelbuttom_frame) #レイアウトをvolume_widgetに突っ込む
    self.gaugelevel_frame=QHBoxLayout() #音量テストをまとめる横方向のレイアウトの作成
    self.gaugelevel_frame.addWidget(self.sldlevel)
    self.gaugelevel_frame.addWidget(self.levelgroup_widget)
    self.gaugelevel_widget=QWidget()
    self.gaugelevel_widget.setLayout(self.gaugelevel_frame) 
    if(self.parent.bar_num == 0): #いま選択している所をチェック
        self.level1.setChecked(True)
    elif(self.parent.bar_num == 1):
        self.level2.setChecked(True)
    else:
        self.level3.setChecked(True)

#    self.mainWidget=QWidget() #音量設定の枠wの作成
    self.mainWidget=QVBoxLayout() #音量テストをまとめる横方向のレイアウトの作成
    self.mainWidget.addWidget(self.message_Widget)
    self.mainWidget.addWidget(self.selectSE_widget)
    self.mainWidget.addWidget(self.volume_widget)
    self.mainWidget.addWidget(self.checklevel_widget)
    self.mainWidget.addWidget(self.gaugelevel_widget)
        

    self.subwindow.setLayout(self.mainWidget) #レイアウトをｗに突っ込む


    #それぞれ押したときの処理　drivesheetに書いてる
    self.noticeEnable.clicked.connect(self.on_clicked_noticeEnable)
    self.message_boxEnable.clicked.connect(self.on_clicked_message_boxEnable)
    self.workHourButton.clicked.connect(self.on_clicked_workHourEdit)
    self.clevel1.clicked.connect(self.on_clicked_clevel1)  
    self.clevel2.clicked.connect(self.on_clicked_clevel2)
    self.clevel3.clicked.connect(self.on_clicked_clevel3)
    self.level1.clicked.connect(self.on_clicked_level1)
    self.level2.clicked.connect(self.on_clicked_level2)
    self.level3.clicked.connect(self.on_clicked_level3)
    
    self.subwindow.show()
