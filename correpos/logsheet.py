from sheet import sheet
import config


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import datetime
import pyaudio
import wave
import cv2
import math
import copy
import pymysql.cursors

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

matplotlib.use("Qt5Agg")

import pandas as pd

# import dbfun

class logSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
                # 映像表示
        #self.logLabel = QLabel(self)
        #self.logLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
        #self.logLabel.move(IMG1_POS[0], IMG1_POS[1])
        

        #self.logLabel.bar(left=x, height=self.data, width=0.3, align='center',alpha=0.44, picker=5)

        self.log_w = QWidget(self)
        
        self.backbutton = QPushButton("戻る",self)
        self.backbutton.clicked.connect(self.on_clicked_back)
        self.changebutton = QPushButton("変更",self)
        self.changebutton.clicked.connect(self.on_clicked_change)
        # self.backbutton.move(0,0)

        self.logLabel = QLabel(self)
        self.logLabel.move(550, 10)
        #self.descLabel.resize(50, 30)
        self.logLabel.setText("今日の記録")

        self.dpi = 100
        self.fig = Figure((10,5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.move(100,40)
        self.canvas.setVisible(False)

        self.combo_y = QComboBox(self)
        self.combo_m = QComboBox(self)
        self.combo_d = QComboBox(self)
        self.yearLabel = QLabel(self)
        self.monthLabel = QLabel(self)
        self.dayLabel = QLabel(self)

        self.yearLabel.setText("年")
        self.monthLabel.setText("月")
        self.dayLabel.setText("日")

        for var in range(2016,2020):
            self.combo_y.addItem(str(var))

        for var in range(1,13):
            self.combo_m.addItem(str(var))

        for var in range(1,32):
            self.combo_d.addItem(str(var))    


        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.backbutton)
        self.hbox.addWidget(self.combo_y)
        self.hbox.addWidget(self.yearLabel)
        self.hbox.addWidget(self.combo_m)
        self.hbox.addWidget(self.monthLabel)
        self.hbox.addWidget(self.combo_d)
        self.hbox.addWidget(self.dayLabel)
        self.hbox.addWidget(self.changebutton)

        # hbox.addWidget()

        self.log_w.setLayout(self.hbox)



 

    def on_clicked_change(self):
        self.countarray_day = np.array([0]*24)
        df = pd.read_csv('log.csv')
        df = df['0']

        print(int(self.combo_d.currentText()))

        for var in range(0,len(df.index)-1):
             if (int(self.combo_d.currentText()) == int(pd.to_datetime(df.values[var]).day)) and (int(self.combo_m.currentText()) == int(pd.to_datetime(df.values[var]).month)) and (int(self.combo_y.currentText()) == int(pd.to_datetime(df.values[var]).year)):
                self.countarray_day[int(pd.to_datetime(df.values[var]).hour)] += 1


        self.axes = self.fig.add_subplot(111)
        # self.data = [1,2,3,1,2,3]
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()

        # x = range(len(self.data))

        # left = np.array([1, 2, 3, 4, 5])
        # height = np.array([100, 200, 300, 400, 500])
        # self.axes.bar(left, height)

        self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)

        # self.axes.title("今日の記録")
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Time")

        # self.axes.bar(left=self.hourlabel, height=self.data, width=0.3, align='center',alpha=0.44, picker=5)
        self.canvas.draw()
        self.canvas.setVisible(True)

        
    def on_clicked_back(self):
        self.parent.setSheet(1)
        self.canvas.setVisible(False)
        self.stop()      


    def stop(self):
        super().stop()
        
    def start(self):
        super().start()
        # self.canvas.draw()
       #pass a figure to the canvas
        d = datetime.datetime.today()
        self.countarray_day = np.array([0]*24)
        self.hour = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        self.hourlabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]


        # connection = pymysql.connect(host='localhost',
        #                          user='root',
        #                          password='password',
        #                          db='crps',
        #                          charset='utf8',
        #                          # cursorclassを指定することで
        #                          # Select結果をtupleではなくdictionaryで受け取れる
        #                          cursorclass=pymysql.cursors.DictCursor)
        # # SQLを実行する
        # with connection.cursor() as cursor:
        #     sql = "SELECT * FROM kuse"
        #     cursor.execute(sql)
        
        #     # Select結果を取り出す
        #     self.results = cursor.fetchall() #result = ((kuse_id xxx, ocu_time yyy) (kuse_id zzz, ocu_time www) ....)
        #     print(self.results)
        #     for r in self.results:
        #         print(r["ocu_time"])
        #         if ((d.day == r["ocu_time"].day) and (d.month == r["ocu_time"].month) and (d.year == r["ocu_time"].year)):
        #             self.countarray_day[r["ocu_time"].hour] += 1
        #         # => {'name': 'Cookie', 'id': 3}
            
        #     connection.close()
        
        # print(self.countarray_day)    
        
        df = pd.read_csv('log.csv')
        df = df['0']

        for var in range(0,len(df.index)-1):
             if ((d.day == pd.to_datetime(df.values[var]).day) and (d.month == pd.to_datetime(df.values[var]).month) and (d.year == pd.to_datetime(df.values[var]).year)):
                self.countarray_day[pd.to_datetime(df.values[var]).hour] += 1


        self.axes = self.fig.add_subplot(111)
        # self.data = [1,2,3,1,2,3]
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()

        # x = range(len(self.data))

        # left = np.array([1, 2, 3, 4, 5])
        # height = np.array([100, 200, 300, 400, 500])
        # self.axes.bar(left, height)

        self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)

        # self.axes.title("今日の記録")
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Time")

        # self.axes.bar(left=self.hourlabel, height=self.data, width=0.3, align='center',alpha=0.44, picker=5)
        self.canvas.draw()
        self.canvas.setVisible(True)