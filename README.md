# HackAichi2021
HackAichiで担当した機械学習のコード

```
.
├── README.md
├── __pycache__
│   └── model.cpython-39.pyc
├── config.txt
├── src
│   ├── img
│   │   └── img.jpg
│   ├── log
│   │   └── log_sample.csv
│   └── py_file
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-39.pyc
│       │   ├── example.cpython-39.pyc
│       │   ├── func.cpython-39.pyc
│       │   └── model.cpython-39.pyc
│       ├── example.py
│       ├── func.py
│       └── model.py
└── test.py
```

img.jpg
* Face Emotion Recognizerのためのファイル. カメラに接続して, 顔を撮影する.

log_sample.csv
* キーボード操作とマウス操作を, 1分ごとに記録したログ. 記録するためのソフトはここにはない.
* 機械学習モデルを最初に学習済みとするためのサンプルファイル.

example.py
* 機械学習モデルの定義.

func.py
* model.pyで使うための関数の定義.

mode.py
* 機械学習を呼び出しやすいよう, モジュール化したもの.

test.py
* 試運転用ファイル.
