# 顔認証式勤怠打刻システム

## 概要

このシステムは、顔認証で勤怠打刻を行います。事前登録した人物がカメラの前に立つと、名前と時間を記録します。


### 開発の経緯

新型コロナウルスの影響により、大学から研究室での入室者名・部屋・入退室時間を記録して欲しいという要請が出ました。従来は、手書きによる記録・管理を行っていましたが、記入漏れや複数人が接触することになる用紙やペンの利用、代理記入などの問題がありました。そこで、これらの問題を解決するためのシステムとして、顔認証方式による勤怠打刻システムを構築しました。

### 特徴

Raspberry Pi*とカメラ、電源があればどこでも設置できます。顔認証方式のため、なりすましの心配がなく、非接触であることから感染症対策にもなります。また、部屋の出入りの際に顔をかざすだけなので、記録漏れのリスクも少ないです。記録された名前と時間は `log.csv` に保存されます。また、認識されたときの顔は `log` フォルダ内に画像として日時と名前付きで保存されます。

※Raspberry Pi以外では動作未確認ですが、依存ライブラリが導入できる環境であれば動作する可能性があります。


## 導入

### リポジトリのクローン

以下のコマンドでリポジトリをクローンしてください。

```bash
$ git clone https://github.com/george-oscar/attendance_management.git
$ cd attendance_management
```

### 依存ライブラリの導入

シェルスクリプトを用いて必要なライブラリをインストールします。個別にインストールしたい方は後述する依存ライブラリを参考にしてください。

```bash
$ ./requirements.sh
```

### 動作確認済環境

* Raspberry Pi 4 Model B
* Raspberry Pi OS Buster
* python 3.7.3
* Open CV 4.0

### 依存ライブラリ

* opencv-python (https://pypi.org/project/opencv-contrib-python/)
* opencv-contrib-python (https://pypi.org/project/opencv-contrib-python/) 
* dlib (http://dlib.net/)
* face_recognition (https://pypi.org/project/face-recognition/)

## 使用方法

1. 顔の撮影

`capture_face.py` を実行して、勤怠を記録したい人物の顔画像を撮影します。プログラムを実行したらローマ字で名前を入力してください。撮影した画像は `faces` フォルダ内に保存されます。

```bash
$ python3 capture_face.py
```

2. configファイルの編集

configファイル `config.json` では、顔認証の際のパラメータを編集できます。namesの項目は必ず変更してください。複数人いる場合は "," で区切って記入してください。

* names: 名前を登録します。`faces` フォルダにある画像の名前と同じ名前を登録してください。
* resolution: 画像撮影時の解像度を指定します。
* framerate: 画像撮影時のフレームレートを指定します。
* face_recognition_ratio: 認識する最小の顔の大きさを画像に対しての比率で指定します。
* face_recognition_interval: 顔を認識する間隔を秒数で指定します。
* display_recognition_face_frames: 認識された顔を表示するフレーム数を指定します。


3. プログラムの実行

以下のコマンドでシステムを稼働させます。

```bash
$ python3 attendance_management.py
```

## ライセンス

This software is released under the MIT License, see LICENSE.