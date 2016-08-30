# -*- coding: UTF-8 -*-

import cv2
import os

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# カメラからキャプチャー
cap = cv2.VideoCapture(0)

color = (255, 255, 255) #白 

while(True):

    # 動画ストリームからフレームを取得
    ret, frame = cap.read()

    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

    for rect in facerect:
        #検出した顔を囲む矩形の作成
        cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)

     # 表示
    cv2.imshow("Show FLAME Image", frame) 

    # qを押したら終了。
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()# -*- coding: UTF-8 -*-

