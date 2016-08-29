import sys
from PyQt5.QtWidgets import (QWidget, QLabel, 
    QLineEdit, QApplication, QHBoxLayout, QPushButton)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 


#画像、映像の縦横サイズ
S_X = 400
S_Y = 300

#画像、映像のポジション
B1_X = 750
B2_X = 100
B1_Y = 150
B2_Y = 150

class Sub(QWidget):
	
	def __init__(subf):
		super().__init__()
		
		subf.secondUI()

	def secondUI(subf):
		subf.setGeometry(200, 300, 1600, 800)
		subf.setWindowTitle('second')	



class Main(QWidget):

	def __init__(self):
		super().__init__()

		
		self.initUI()


	def initUI(self):  
		#カメラキャプチャ    
		self.cap = cv2.VideoCapture(0)
		
		#撮影前の画像（右
		self.image = QImage("enemy1.png")
		
		self.pixmap = QPixmap.fromImage(self.image)
		self.label1 = QLabel(self)	#撮影画像用のラベル
		self.label2 = QLabel(self)	#カメラ映像用のラベル
		
		self.label1.setPixmap(self.pixmap)
		#撮影画像のリサイズ、移動
		self.label1.resize(S_X,S_Y)
		self.label1.move(B1_X,B1_Y)
		
		#カメラ映像の表示位置移動
		self.label2.move(B2_X,B2_Y)
		
		#撮影ボタン、決定ボタンの作成、リサイズ、移動
		self.button1 = QPushButton('shot', self)
		self.button2 = QPushButton('decide', self)
		self.button1.resize(200, 50)
		self.button1.move(200, 500)
		self.button2.resize(200, 50)
		self.button2.move(850, 500),
		
		
		self.button1.clicked.connect(self.buttonClicked)
		self.button2.setEnabled(False)
		self.button2.clicked.connect(QCoreApplication.instance().quit)
		#self.button2.clicked.connect(self.buttonnext)
	
		self.setGeometry(200, 300, 1200, 600)
		self.setWindowTitle('init')	
		#self.show()


	









	#カメラ映像関連
	def paintEvent(self,event):
		
		ret, frame1 = self.cap.read()
		
		color = (255, 255, 255) #白
		#物体認識（顔認識）の実行
		facerect = cascade.detectMultiScale(frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
		#座標取得
		for rec in facerect:
			self.x = rec[0]	#x座標
			self.y = rec[1]	#y座標

		for rect in facerect:
			#検出した顔を囲む矩形の作成
			cv2.rectangle(frame1, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)

		
		
		
		
		
		frame2 = cv2.resize(frame1,(S_X,S_Y))
		self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)#QPixmap("photo.jpg")
		pix.scaled(300,300)
		self.label2.resize(S_X,S_Y)
		self.label2.setPixmap(pix)


	#撮影ボタンクリック時のイベント
	def buttonClicked(self):
		self.button2.setEnabled(True)
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)#QPixmap("photo.jpg")
		pix.scaled(300,300)
		self.label1.resize(S_X,S_Y)
		self.label1.setPixmap(pix)
		self.button1.setText("reshot")
		print(self.y)
		



def main(args):
	app = QApplication(args)
	win = Main()
	win.show()
	sys.exit(app.exec_())
	



if __name__ == '__main__':
	main(sys.argv)
	
	#app = QApplication(sys.argv)
	#app2 = QApplication(sys.argv)
	#ex = Main()
	#ex2 = Sub()
	#sys.exit(app.exec_())
	#sys.exit(app2.exec_())