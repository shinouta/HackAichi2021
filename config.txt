.
├── README.txt
├── __pycache__
│   └── model.cpython-39.pyc
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── example.cpython-39.pyc
│   │   ├── func.cpython-39.pyc
│   │   └── model.cpython-39.pyc
│   ├── example.py
│   ├── func.py
│   ├── log
│   │   └── log_sample.csv
│   └── model.py
└── test.py

test.py
  modelモジュールの使い方の例を示した

__pycache__
  モジュールのimportを効率よくするためのものらしい. 自動生成につき触らないで良い

src
  色々な関数や初期logをまとめた
  WorkExample型のインスタンスを生成するたび, log_sample.csvを読み込んで学習済み状態のモデルを生成する.

mode.py
  機械学習をしやすくしたMachine_Learinigクラスがある.
  __init__メソッドに初期学習(インスタンス生成したときの, 学習済みにするやつ)の結果を出力するコードがコメントアウトされてるので, 適宜#を消して実行されたい.


メソッド紹介:
load_new_log_and_get_exp(log: list)
  logの書式は以下の通り
  log = [id: str, data: str, keyboard: str, mouse: str, click: str, label: str]
  これを実行すると, 各種ステータスを計算し(出力はしない), int型の経験値を出力する

get_status_of系
  引数不要でint型のステータスを出力する.
