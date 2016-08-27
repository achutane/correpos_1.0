import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPixmap
import cv2

X = 1200
Y  = 600

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.camera()
		self.initUI()
		
		

		
	def initUI(self,mirror=True, size=None):
	    # 画面サイズ設定
		self.setFixedSize(X, Y)
		# x=300,y=300の場所へ画面を移動
		self.move(300, 200)
		# タイトルを設定
		self.setWindowTitle('Simple')
		button1 = QPushButton('button', self)
		button2 = QPushButton('finish', self)
		button1.resize(200, 50)
		button1.move(200, 500)
		button2.resize(200, 50)
		button2.move(800, 500)

		image = cv2.imread("photo.jpg")
		cv2.imshow("img",image)
		



	def camera(self, mirror=True, size=None):
		cap = cv2.VideoCapture(0)

		while True:
			ret, frame = cap.read()

			if mirror is True:
				frame = frame[:,::-1]

			if size is not None and len(size) == 2:
				frame = cv2.resize(frame, (100,100))

			cv2.imshow('camera capture', frame)

			key = cv2.waitKey(1) & 0xFF

			# qが押された場合は終了する
			if key == ord('q'):
				break
    		# sが押された場合は保存する
			if key == ord('s'):
				path = "photo.jpg"
				#cv2.imwrite(path,frame)
				break;

		cap.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Window()
	ex.show()
	sys.exit(app.exec_())  