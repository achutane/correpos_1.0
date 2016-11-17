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
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class logSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
     # 映像表示
        self.log_w = QWidget(self)

        self.monthbutton = QPushButton("今月",self)
        self.monthbutton.move(900,8)
        self.monthbutton.clicked.connect(self.on_clicked_backtomonth)

        self.daybutton = QPushButton("今日",self)
        self.daybutton.move(1000,8)
        self.daybutton.clicked.connect(self.on_clicked_backtoday)

        self.changebutton = QPushButton("指定日に変更",self)
        self.changebutton.clicked.connect(self.on_clicked_change)

        self.logLabel = QLabel(self)
        self.logLabel.move(500, 15)
        self.logLabel.setText('<h2>記録<h2>')

        self.dpi = 100
        self.fig = Figure((11,5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.canvas.move(0,40)
        self.canvas.setVisible(False)
        
        self.yearLabel = QLabel(self)
        self.monthLabel = QLabel(self)
        self.dayLabel = QLabel(self)
        self.yearLabel.setText("年")
        self.monthLabel.setText("月")
        self.dayLabel.setText("日")

        self.combo_y = QComboBox(self)
        self.combo_m = QComboBox(self)
        self.combo_d = QComboBox(self)
        for var in range(2016,2050):
            self.combo_y.addItem(str(var))

        for var in range(1,13):
            self.combo_m.addItem(str(var))

        for var in range(1,32):
            self.combo_d.addItem(str(var))    
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.combo_y)
        self.hbox.addWidget(self.yearLabel)
        self.hbox.addWidget(self.combo_m)
        self.hbox.addWidget(self.monthLabel)
        self.hbox.addWidget(self.combo_d)
        self.hbox.addWidget(self.dayLabel)
        self.hbox.addWidget(self.changebutton)
        self.log_w.setLayout(self.hbox)


    def on_clicked_change(self):

        self.countarray_day = np.array([0]*24)
        self.hour = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        self.hourlabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        df = pd.read_csv('log.csv')
        df = df['0']
        for var in range(0,len(df.index)-1):
             if (int(self.combo_d.currentText()) == int(pd.to_datetime(df.values[var]).day)) and (int(self.combo_m.currentText()) == int(pd.to_datetime(df.values[var]).month)) and (int(self.combo_y.currentText()) == int(pd.to_datetime(df.values[var]).year)):
                self.countarray_day[int(pd.to_datetime(df.values[var]).hour)] += 1

        self.axes = self.fig.add_subplot(111)
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()

        self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Time ("+str(self.combo_y.currentText())+"/"+str(self.combo_m.currentText())+"/"+str(self.combo_d.currentText())+")")
        self.canvas.draw()
        self.canvas.setVisible(True)


    def on_clicked_backtomonth(self):

        self.start() 


    def on_clicked_backtoday(self):

        d = datetime.datetime.today()
        year=d.strftime("%Y")
        month=d.strftime("%m")
        day=d.strftime("%d") 
        self.countarray_day = np.array([0]*24)
        self.hour = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        self.hourlabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]
        df = pd.read_csv('log.csv')
        df = df['0']

        for var in range(0,len(df.index)-1):
             if ((d.day == pd.to_datetime(df.values[var]).day) and (d.month == pd.to_datetime(df.values[var]).month) and (d.year == pd.to_datetime(df.values[var]).year)):
                self.countarray_day[pd.to_datetime(df.values[var]).hour] += 1

        self.axes = self.fig.add_subplot(111)
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()
        self.axes.bar(self.hour,self.data,tick_label = self.hourlabel, align = "center",width = 0.4)
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Time ("+year+"/"+month+"/"+day+")")
        self.canvas.draw()
        self.canvas.setVisible(True)



    def stop(self):
        super().stop()

        
    def start(self):
        super().start()

        d = datetime.datetime.today()
        year=d.strftime("%Y")
        month=d.strftime("%m")
        self.countarray_day = np.array([0]*32)
        self.day = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
        self.daylabel = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
        df = pd.read_csv('log.csv')
        df = df['0']

        for var in range(0,len(df.index)-1):
            if ((d.month == pd.to_datetime(df.values[var]).month) and (d.year == pd.to_datetime(df.values[var]).year)):
                self.countarray_day[pd.to_datetime(df.values[var]).day] += 1

        self.axes = self.fig.add_subplot(111)
        self.data = self.countarray_day
        self.axes.clear()
        self.axes.grid()
        self.axes.bar(self.day,self.data,tick_label = self.daylabel, align = "center",width = 0.4)
        self.axes.set_ylabel("frequency")
        self.axes.set_xlabel("Day ("+year+"/"+month+")")
        self.canvas.draw()
        self.canvas.setVisible(True)