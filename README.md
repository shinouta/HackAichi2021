# HackAichi2021
HackAichi2021で担当した機械学習のコード

###制作物の概要
* 社員の仕事の進捗に応じて, キャラが育つ.
* キャラの育ち方で, 社員の仕事の個性が分かる.
* リモートワークでも, キャラが育っているかどうかで, 上司は社員の仕事の進捗を確認できる.

###ソースコードの概要
* 社員のキーログを1分毎に取得して, 働いているかどうかの判定と, 経験値とステータスを出力する. 出力した経験値とステータスの処理はここではなくDjango側で行った.
* modelモジュールをimport→1分毎のキーログを渡して, 機械学習の結果(経験値とステータス)を出力する.
* log_sample.csvはラベル付き, つまり働いているか働いていないかが既に分かっているデータ. これを教師データとして利用する.
* test.pyにてlog_sample.csvを確認用データとして再度用いている. また, 数が多いため, if文を使って働いているときだけの結果を出力している.

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
