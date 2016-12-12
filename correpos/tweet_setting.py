import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton) 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from glob import glob
from os.path import join, relpath
import tweepy
import webbrowser






def tweet_setting(self):
    self.subwindow_t = QWidget()  
    self.subwindow_t.setWindowTitle("tweet_setting")
    self.subwindow_t.setWindowIcon(QIcon('img/correpos_icon.png')) #iconをそろえた
    self.subwindow_t.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint) #最大化以外のボタンを有効

    self.auth_button = QPushButton("アプリ認証",self)
    self.auth_button.clicked.connect(self.on_clicked_auth)
    self.error_text = QLabel()
    self.error_text.setText("")
    self.key_input = QLineEdit("番号を入力してください",self)
    self.key_generate = QPushButton("完了",self)
    self.key_generate.setEnabled(False)
    self.key_generate.clicked.connect(self.on_clicked_generate)
    self.attention_text00 = QLabel()  #例外処理がうまくいかないからとりあえず注意喚起
    self.attention_text00.setText("注意：")
    self.attention_text01 = QLabel()
    self.attention_text01.setText("errorになった場合，twitterの再設定に")
    self.attention_text11 = QLabel()
    self.attention_text11.setText("アプリの再起動が必要になります")
    self.attention_grid=QGridLayout() #グリッド作成
    self.attention_grid.addWidget(self.attention_text00, 0, 0)
    self.attention_grid.addWidget(self.attention_text01, 0, 1)
    self.attention_grid.addWidget(self.attention_text11, 1, 1)
    self.attention_Widget=QWidget(self)
    self.attention_Widget.setLayout(self.attention_grid) 

    self.key_widget = QWidget()
    self.key_layout = QHBoxLayout()
    self.key_layout.addWidget(self.key_input)
    self.key_layout.addWidget(self.key_generate)
    self.key_widget.setLayout(self.key_layout)
   	
    self.tweet_layout = QVBoxLayout()
    self.tweet_layout.addWidget(self.auth_button)
    self.tweet_layout.addWidget(self.error_text)
    self.tweet_layout.addWidget(self.key_widget)
    self.tweet_layout.addWidget(self.attention_Widget)

    self.subwindow_t.setLayout(self.tweet_layout)


    self.subwindow_t.show()








