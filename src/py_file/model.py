from . import func
import numpy as np
from fer import FER
import cv2
import time
from sklearn import svm
from sklearn.metrics import confusion_matrix

class Machine_Learning(object):
    def __init__(self):
        self.model = self.learn_examples()
        self.status = [0.0]*4
        self.confused = 0

    def learn_examples(self):
        """
        arg ->      None
        return ->   学習済みモデル
        note:       src/log/log_sample.csvを参照して学習済みモデルを作成する.
        """
        ex = func.build_examples_by_filename('src/log/log_sample.csv')
        train_set, devel_set = func.divide80_20(ex)

        train_vecs = np.array([e.get_features() for e in train_set])
        train_labels = [e.get_label() for e in train_set]
        devel_vecs =  np.array([e.get_features() for e in devel_set])
        devel_labels = [e.get_label() for e in devel_set]

        #model = neighbors.KNeighborsClassifier(5)
        model = svm.SVC(probability=True, C=2)
        model.fit(train_vecs, train_labels)
        
        #devel_predicted = model.predict(devel_vecs)
        #cm=confusion_matrix(devel_labels, devel_predicted, labels=['work', 'not work']) # 混同行列 
        #true_neg, false_pos, false_neg, true_pos = cm.flatten()
        #print(cm)
        #stats = func.get_stats(true_pos, false_pos, true_neg, false_neg)

        return model

    def load_new_log(self, log):
        """
        arg ->      log: list
        return ->   exp: int
        note:       log = [id: str,date: str, keyboard: str, mouse: str, click: str, (label: str)]という6次元リストを引数とする.

        """
        # 読み込んだログからWorkExamole型のオブジェクトを1つ生成
        example_log = func.build_examples_by_log(log)
        # 生成したオブジェクトの特徴ベクトルを取得
        features_log = example_log.get_features()

        # Confused Bar用の写真撮影
        self.take_selfy()
 
        # 経験値, 各種ステータスの計算
        self.calc_exp(features_log)
        self.calc_Speed(features_log)
        self.calc_Accuracy(features_log)
        self.calc_Efficiency(features_log)
        self.calc_Concentration(features_log)
        self.calc_Confused_Point()

    def take_selfy(self):
        """
        arg ->      None
        return ->   None
        note:       Confused Pointのための写真を撮るだけ
        """
        capture = cv2.VideoCapture(0)
        time.sleep(1)
        is_taken, image = capture.read()
        if is_taken:
            cv2.imwrite("src/img/img.jpg", image) 

    def calc_Confused_Point(self):
        """
        arg ->      None
        return ->   None
        note:       Confused Pointを計算する. 値は返さない
        """
        try:
            image = cv2.imread("src/img/img.jpg")
            emo_detector = FER(mtcnn=True)
            # Capture all the emotions on the image
            captured_emotions = emo_detector.detect_emotions(image)
            confused = int((captured_emotions[0]['emotions']['angry']\
                        + captured_emotions[0]['emotions']['disgust']\
                        + captured_emotions[0]['emotions']['fear']\
                        + captured_emotions[0]['emotions']['sad'])*30)
            if confused == 0:
                confused = -5
        except:
            confused = -5
        self.confused += confused
        if self.confused < 0:
            self.confused = 0

    def calc_Speed(self, features_log):
        """
        arg ->      features_log: list
        return ->   None
        note:       ステータスSpeedを計算する. features_logは, 新しく読み込んだlogから得た特徴ベクトル. Speedの上限, 下限はそれぞれ100, 0
        """
        self.status[0] = int(features_log[0]*100)*3
        if self.status[0] > 100:
            self.status[0] = 100

    def calc_Accuracy(self, features_log):
        """
        arg ->      features_log: list
        return ->   None
        note:       ステータスAccuracyを計算する. features_logは, 新しく読み込んだlogから得た特徴ベクトル. Accuracyの上限, 下限はそれぞれ100, 0
        """
        self.status[1] = int((100 - features_log[1]*100)*features_log[0])*3
        if self.status[1] > 100:
            self.status[1] = 100

    def calc_Efficiency(self, features_log):
        """
        arg ->      features_log: list
        return ->   None
        note:       ステータスEfficiencyを計算する. features_logは, 新しく読み込んだlogから得た特徴ベクトル. Efficiencyの上限, 下限はそれぞれ100, 0
        """
        self.status[2] = int(features_log[2]*100)*3
        if self.status[2] > 100:
            self.status[2] = 100

    def calc_Concentration(self, features_log):
        """
        arg ->      features_log: list
        return ->   None
        note:       ステータスConcentrationを計算する. features_logは, 新しく読み込んだlogから得た特徴ベクトル. Concentrationの上限, 下限はそれぞれ100, 0
        """
        self.status[3] = int(self.get_exp()*0.5 + features_log[3]*50)*3
        if self.status[3] > 100:
            self.status[3] = 100

    def calc_exp(self, features_log):
        """
        arg ->      features_log: list
        return ->   None
        note:       features_logは, 新しく読み込んだlogから得た特徴ベクトル. expの上限, 下限はそれぞれ100, 0
        """
        vecs_log = np.array([features_log])
        prb_not_work, prb_work = self.model.predict_proba(vecs_log)[0]
        exp = int(80*prb_work**5 + 20 - prb_not_work*100)
        if exp < 0:
            exp = 0
        self.exp = exp

    def get_status_of_Speed(self):
        """
        arg ->      None
        return ->   Speed: int
        note:       ステータスSpeedを返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.status[0]

    def get_status_of_Accuracy(self):
        """
        arg ->      None
        return ->   Accuracy: int
        note:       ステータスAccuracyを返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.status[1]

    def get_status_of_Efficiency(self):
        """
        arg ->      None
        return ->   Efficiency: int
        note:       ステータスEfficiencyを返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.status[2]

    def get_status_of_Concentration(self):
        """
        arg ->      None
        return ->   Concentration: int
        note:       ステータスConcentrationを返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.status[3]

    def get_status_of_all(self):
        """
        arg ->      None
        return ->   [Speed, Accuracy, Efficiency, Concentration]: list
        note:       ステータスを4次元リストで返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.status

    def get_exp(self):
        """
        arg ->      None
        return ->   exp: int
        note:       経験値expを返す. 上限, 下限はそれぞれ100, 0.
        """
        return self.exp

    def get_Confused_Point(self):
        """
        arg ->      None
        return ->   Confused_Point: int
        note:       お困りメーターを貯めるためのポイントを返す. 通常時は-1となる.
        """
        return self.confused

    def get_is_Confused(self):
        """
        arg ->      None
        return ->   is_Confused: bool
        note:       お困りかどうかを返す. 通常時False
        """
        return self.confused >= 60
