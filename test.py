from src.py_file.model import Machine_Learning
import csv

m = Machine_Learning()
csv_file = open("src/log/log_sample.csv", encoding="utf-8") #このデータは初期学習のデータだが, テスト用に再利用している
i = 0
for line in csv.reader(csv_file):
    if line[-1] == "o" and i < 5:
        m.load_new_log(line) #ログを読み込み
        print("status =", m.get_status_of_all()) #ステータスを表示
        print("exp =", m.get_exp())
        print("Confused =", m.get_Confused_Point())
        print() #見やすく空白行を挿入
        i += 1
