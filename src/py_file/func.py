#関数群
def accuracy(true_pos, false_pos, true_neg, false_neg): # 正解率・正確度
    try:
        numerator = true_pos + true_neg
        denominator = true_pos + true_neg + false_pos + false_neg
        return numerator / denominator
    except ZeroDivisionError:
        return float('nan')    

def recall(true_pos, false_neg): # 再現率，感度
    try:
        return true_pos / (true_pos + false_neg)
    except ZeroDivisionError:
        return float('nan')
    
def specificity(true_neg, false_pos): # 特異度
    try:
        return true_neg / (true_neg + false_pos)
    except ZeroDivisionError:
        return float('nan')
    
def precision(true_pos, false_pos): # 適合率
    try:
        return true_pos / (true_pos + false_pos)
    except ZeroDivisionError:
        return float('nan')
    
def f1_score(precision, recall): # F1値
    try:
        return 2 * precision * recall / (precision + recall)
    except ZeroDivisionError:
        return float('nan')

# 上記，評価値を一度に計算
def get_stats(true_pos, false_pos, true_neg, false_neg, to_print = True):
    acc = accuracy(true_pos, false_pos, true_neg, false_neg)
    rec = recall(true_pos, false_neg)
    spec = specificity(true_neg, false_pos)
    pre = precision(true_pos, false_pos)
    f = f1_score(pre, rec)    
    if to_print:
        print(' Accuracy =', round(acc, 3))
        print(' Recall (Sensitivity) =', round(rec, 3))
        print(' Specificity =', round(spec, 3))
        print(' Precision =', round(pre, 3))
        print(' F1 =', round(f, 3))
    return (acc, rec, spec, pre, f)


# キーロガーなどから送られてきたcsvファイルを処理するための関数群
def convert_key_to_list(key_line: str) -> list:
    """
    keyの文字列を受け取って、特殊キーはまとまったまま、英数字は1文字ずつリスト化
    """
    l = []
    if key_line:
        element = ""
        now_in_brackets = False
        for s in key_line:
            if s == "【":
                now_in_brackets = True
            elif s == "】":
                now_in_brackets = False
                l.append(element)
                element = ""
            elif now_in_brackets:
                element += s
            else:
                l.append(s)
    return l

def convert_mouse_to_list(mouse_line: str) -> list:
    """
    mouseの文字列を受け取って、[x, y]形式の二次元座標をappendしてリスト化
    """
    l = []
    if mouse_line:
        element = ""
        mouse_line = mouse_line.split(",")
        for s in mouse_line: 
            l.append(list(map(int, s.split(":"))))

    return l

def convert_click_to_list(click_line: str) -> list:
    """
    clickの文字列を受け取って、[x, y] 形式の二次元座標をappendしてリスト化
    """
    l = []
    if click_line:
        element = ""
        click_line = click_line.split(",")
        for s in click_line:
            tmp = s.split("_")[1]
            l.append(list(map(int, tmp.split(":"))))
    return l

import csv
import random
from .example import WorkExample

def divide80_20(examples):
    """データを8対2にランダムに分割"""
    random.seed(0)
    sample_indices = random.sample(range(len(examples)), len(examples) // 5) 
    training_set, test_set = [], []
    for i in range(len(examples)):
        if i in sample_indices:
            test_set.append(examples[i])
        else:
            training_set.append(examples[i])
    return training_set, test_set

def build_examples_by_filename(file_name):
    """
    csvファイルからデータを読み込み, WorkExample型が入ったリストexamplesを返す
    """
    examples = []

    csv_file = open(file_name, encoding="utf-8")

    for line in csv.reader(csv_file):
        line_sliced = line[2:]
        for i in range(len(line_sliced)):
            if i == 0:
                keyboard = convert_key_to_list(line_sliced[i])
            if i == 1:
                mouse = convert_mouse_to_list(line_sliced[i])
            if i == 2:
                click = convert_click_to_list(line_sliced[i])
            if i == 3:
                label = line_sliced[i]

        data = [keyboard, mouse, click, label]
        examples.append(WorkExample(data))
        data = []
        keyboard = []
        mouse = []
        click = []

    return examples

def build_examples_by_log(log):
    """
    log = [
    id: str,
    date: str,
    keyboard: str,
    mouse: str,
    click: str,
    label: str]
    という6次元のlogを受け取り, WorkExample型を返す
    """
    line_sliced = log[2:]
    for i in range(len(line_sliced)):
        if i == 0:
            keyboard = convert_key_to_list(line_sliced[i])
        if i == 1:
            mouse = convert_mouse_to_list(line_sliced[i])
        if i == 2:
            click = convert_click_to_list(line_sliced[i])
        if i == 3:
            label = line_sliced[i]
    
    data = [keyboard, mouse, click, label]
    return WorkExample(data)
