# HackAichi2021
HackAichi2021にて担当した制作物における, 機械学習部分のコードです.　勤務中のキーログと表情を, ステータスや経験値に変換し, 出力します.


## 制作物の概要
* リモートワークにおける, 「自宅だとやる気がでない」「社員の進捗を管理し辛い」という問題を解決するためのサービス.
* 社員の仕事の進捗に応じて, キャラが育つ.
* キャラの育ち方で, 社員の仕事の個性が分かる.
* キャラが育っているかどうか、どのように育ったか,　などによって上司は社員の仕事の進捗を管理できる.
* 社員が困った顔をしていたら, キャラにその様子が反映され, 助け合いを促す.

## 担当ソースコードの概要
* 社員のキーログを1分毎に取得して, 働いているかどうかの判定と, 経験値とステータスを出力する. 出力した経験値とステータスの処理はここではなくDjango側で行った.
* modelモジュールをimport→1分毎のキーログを渡して, 機械学習の結果(経験値とステータス)を出力する.
* log_sample.csvはラベル付き, つまり働いているか働いていないかが既に分かっているデータ. これを教師データとして利用する.
* test.pyにてlog_sample.csvを確認用データとして再度用いている. また, 数が多いため, if文を使って働いているときだけの結果を出力している.

## requirements
```
pip3 install tensorflow
pip3 install fer
pip3 install sklearn
pip3 install opencv-python
```
note: たくさんの警告が出ますが, [この議論](https://github.com/Homebrew/homebrew-core/issues/76621)によると問題がないらしいです.

## 使い方
* 試運転用ファイル`test.py`は以下のようになっています.

```Python

from src.py_file.model import Machine_Learning
import csv

m = Machine_Learning()
csv_file = open("src/log/log_sample.csv", encoding="utf-8") #このデータは初期学習のデータだが, テスト用に再利用している
i = 0
for line in csv.reader(csv_file):
    if line[-1] == "o" and i < 5:
        m.load_new_log(line) #ログを機械学習モデルへ読み込み
        print("status =", m.get_status_of_all()) #ステータスを表示
        print("exp =", m.get_exp()) #経験値を表示
        print("Confused =", m.get_Confused_Point()) #お困り度を表示
        print() #見やすく空白行を挿入
        i += 1

```

* `from src.py_file.model import Machine_Learning`について, `model.py`から必要な機械学習モデルをインポートしています.
* `m = Machine_Learning()`によって, 機械学習モデルを初期化します. この時点で学習済みです.
* `csv_file = open(...)`によって, テストデータを読み込みます. 読みこんでいるデータは, 1分毎に記録したキーログです.　本来ならば別ソフトでこのデータを生成するのですが, 今回はそのソフトがないので, 適当なデータ`log_sample.csv`を読み込ませてあります.
* `if line[-1] == "o" and i < 5:`について、　これは`log_sample.csv`が749行であり, 全てを出力すると大変長くなってしまいます. そのため`line[-1] == o`つまり仕事をしているときのキーログの解析結果(ステータスや経験値など)を5回だけ出力するようにしています.
* statusは`[Speed, Accuracy, Efficiency, Concentration]`のような要素です.
* お困り度は, fer(Face Emotion Recognizer)によって負の感情を取り出し, 上限が100となるように正規化した値です. 「社員が困った顔をしていたら, キャラにそれが反映される」という機能の実現のため, 実装しました.


## ファイル構成

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

`img.jpg`
* Face Emotion Recognizerで生成されるファイル. エラーを起こさないよう, 別の同名ファイルを挿入してあります.

`log_sample.csv`
* キーボード操作とマウス操作を, 1分ごとに記録したログ. 記録するためのソフトは別メンバーが担当したため, ここにはありません.
* 機械学習モデルを学習済みとするためのサンプルファイルです.

`example.py`
* 用いた機械学習モデルの定義. 今回はSVM(Support Vector Machine)を用いた.

`func.py`
* `model.py`にて使った関数群を定義.

`model.py`
* 「顔を撮影し, ステータスと経験値を出力する」という機能を, `import model`とするだけで使えるようにしたファイル。

`test.py`
* 試運転用ファイル.
