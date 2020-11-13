# -*- coding:utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
名前: 顔認証式勤怠打刻システム
目的: 非接触型生体認証による出退勤時間の記録を行う
手順:
	1. フレーム内に写る顔を認識
	2. 認識した顔が事前登録された人物であるか判定
	3. 登録された人物の場合は判定した時刻を記録
実行コマンド:
    python3 attendance_management.py
著者: George Oscar
作成日:2020/11/02
更新日:2020/11/12
---------------------------------------------------------------------------------------------------
"""

print("\n [INFO] モジュールをインポート中．．．")

import os
import csv
import json
import face_recognition
import cv2
import numpy as np
import time
import datetime

print(" [INFO] データをロード中．．．")

# パラメータの設定
font = cv2.FONT_HERSHEY_SIMPLEX
counter = 0
face_img = np.zeros(1)
bef_time = 0
color = (0, 255, 0)

# configファイルの設定
config_path = os.path.dirname(os.path.abspath(__file__)) + '/config.json'

# 出力先の設定
output_csv_path = os.path.dirname(os.path.abspath(__file__)) + '/log.csv'
output_img_path = os.path.dirname(os.path.abspath(__file__)) + '/log'

# configファイルの読み込み
try:
    cfg = json.load(open(config_path, 'r'))   # jsonファイルの読み取り
except:
    print("\n [ERROR] config.jsonの読み取りに失敗")   # エラー処理
    cfg = None

# configファイルで指定したパラメータの設定
names = cfg['names']
face_recognize_ratio = cfg['face_recognition_ratio']
interval = cfg['face_recognition_interval']
span = cfg['display_recognized_face_frames']

# 顔認識用モジュールの呼び出し
known_face_names = names
images = ["{}_image".format(name) for name in names]
known_face_encodings = ["{}_face_encoding".format(name) for name in names]

for i in range(len(images)):
    images[i] = face_recognition.load_image_file("faces/{}.jpg".format(names[i]))
    known_face_encodings[i] = face_recognition.face_encodings(images[i])[0]


# カメラの初期設定
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cfg['resolution'][0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg['resolution'][1])
cam.set(cv2.CAP_PROP_FPS, cfg['framerate'])

# 変数の初期化
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

print("\n [INFO] 勤怠管理を開始しました。終了するには 'ESC' キーを押してください。\n")

# メイン処理文
while cam.isOpened():
    # カメラからフレームを取得
    ret, flame = cam.read()
    flame = cv2.flip(flame, 1)

    # 軽量化のためフレームを縮小
    small_frame = cv2.resize(flame, (0, 0), fx=0.25, fy=0.25)

    # BGRからRGBに変換
    rgb_small_frame = small_frame[:, :, ::-1]

    # 軽量化のため１フレームおきに処理
    if process_this_frame:
        # フレーム内に写る全ての顔を認識
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 事前登録された顔か判定
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # 結果を表示
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 縮小した分の結果を補正
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 座標の変換
        x = left
        y = top
        w = right - left
        h = bottom - top

        # 時間を記録
        date = datetime.datetime.now().strftime("%Y/%m/%d")
        time_ = datetime.datetime.now().strftime("%H:%M:%S")
        now_time=time.time()
        data = {'Date': '{}'.format(date)}

        # 結果を保存 
        if int(now_time) - bef_time > interval:
            bef_time = int(now_time)
            if name == "Unknown":
                break
            else:
                print(" [INFO] {} {} {} さんの情報を記録しました。".format(date, time_, name))

                data_temp = {'Time': '{}'.format(time_), 'Name': '{}'.format(name)}
                data.update(data_temp)

                # csvにログを保存
                if not os.path.exists(output_csv_path):
                    with open(output_csv_path, 'w', newline="") as f:
                        writer = csv.DictWriter(f, data.keys())
                        writer.writeheader()
                        writer.writerow(data)
                else:
                    with open(output_csv_path, 'a', newline="") as f:
                        writer = csv.DictWriter(f, data.keys())
                        writer.writerow(data)


                # 認識した顔画像をjpgで保存 
                filename = "{}/{}_{}.jpg".format(output_img_path, datetime.datetime.now().strftime("%Y%m%d%H%M%S"), name)
                gray = cv2.cvtColor(flame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(filename, gray[y:y+h,x:x+w])
                face_img = flame[y:y+h,x:x+w]
                rec_name = name
            
        # 認識された顔を枠で囲う
        img = flame.copy()
        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)

    # 顔が検出されれば左上にその顔を表示
    if len(face_img) > 1:
        counter += 1
        face_img_resized = cv2.resize(face_img, (100, 100))
        height, width = face_img_resized.shape[:2]
        img[10:10+height, 10:10+width] = face_img_resized        
        if span <= counter:
            counter = 0
            face_img = np.zeros(1)
            rec_name = ""

        cv2.putText(img, str(rec_name), (15,130), font, 1, (255,255,255), 2) 
    
    # ウィンドウで結果を表示
    cv2.namedWindow('Attendance Management', cv2.WINDOW_NORMAL)
    cv2.imshow('Attendance Management', img) 

    # 'ESC' キーで終了
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# 処理を終了
cam.release()
cv2.destroyAllWindows()
print("\n [INFO] 勤怠管理を終了しました。")
