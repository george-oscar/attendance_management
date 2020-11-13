# -*- coding:utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
名前: 顔画像ß撮影プログラム
目的: 顔認証に使用する画像を撮影
手順:
	1. カメラの前に立つ
	2. 登録する人物の名前（ローマ字入力）を登録
	3. 撮影した画像を保存
実行コマンド:
    python3 capture_face.py
著者: George Oscar
作成日:2020/11/12
更新日:2020/11/12
---------------------------------------------------------------------------------------------------
"""

import cv2

# カメラの初期設定
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 名前の入力
name = input('\n 登録する人物の名前をローマ字で入力してください ==>  ')
print("\n [INFO] 撮影します．カメラの正面を向いてお待ち下さい...")

ret, img = cam.read()
cv2.imwrite("faces/" + str(name) + ".jpg", img)


# Do a bit of cleanup
print("\n [INFO] 撮影しました．プログラムを終了します．")
cam.release()
cv2.destroyAllWindows()


