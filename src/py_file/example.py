class Example(object):
    def __init__(self, data: list, label=None):
        self.features = self.calc_features(data)
        self.label = self.set_label(label)
        
    def calc_features(self, data):
        pass
    
    def set_label(self, label):
        return label
 
    def dimensionality(self):
        return len(self.features)
    
    def get_features(self):
        return self.features
    
    def get_label(self):
        return self.label
    
    def __str__(self):
        return str(self.get_features()) + ':'+str(self.get_label())

class WorkExample(Example):
    def __init__(self, line):
        data = line[:-1] # dataは[keyboard: list, mouse: list, click: list]
        label = line[-1] # labelは"work"または"not work"
        super().__init__(data, label)
    
    def calc_features(self, data):
        """
        arg ->      [keyboard: list, mouse: list, click: list, (label: str)]
        return ->   特徴ベクトル: list 
        """
        #特徴ベクトル
        try:
            features = []
            keyboard = data[0]
            mouse = data[1]
            click = data[2]

            features += self.get_keyboard_per_minute_feature(keyboard)
            features += self.get_backspace_and_delete_times_feature(keyboard)
            features += self.get_shortcut_times_feature(keyboard)
            features += self.get_moving_of_mouse_and_click_feature(mouse, click)
        except:
            features = [0.0, 0.0, 0.0, 0.0]

        return features

    def get_keyboard_per_minute_feature(self, keyboard):
        """
        arg ->      keyboard: list
        return ->   [1分あたりのタイピング数/100: float]
        note:       下限, 上限はそれぞれ0.0, 1.0
        """
        feature = []
        value = float(len(keyboard)/100)
        if value > 1.0:
            value = 1.0
        feature.append(value)

        return feature

    def get_backspace_and_delete_times_feature(self, keyboard):
        """
        arg ->      keyboard: list
        return ->   [(<backspace>の回数 + <delete>の回数)*タイピング数/20: float]
        note:       下限, 上限はそれぞれ0.0, 1.0
        """
        feature = []

        count = 0
        for key in keyboard:
            if key == "backspace" or keyboard == "delete":
                count += 1
        
        value = float(count)/20
        if value > 1.0:
            value = 1.0
        feature.append(value)

        return feature

    def get_shortcut_times_feature(self, keyboard):
        """
        arg ->      keyboard: lsit
        return ->   [<Ctrl>と<Alt>の回数/10: float]
        note:       下限, 上限はそれぞれ0.0, 1.0
        """
        feature = []

        count = 0
        for key in keyboard:
            if key == "ctrl" or key == "alt":
                count += 1

        value = float(count)/10
        if value > 1.0:
            value = 1.0
        feature.append(value)

        return feature

    def get_moving_of_mouse_and_click_feature(self, mouse, click):
        """
        arg ->      mouse: list, click: list
        return ->   [マウス移動距離/100000 + click数/20: float]
        note:       下限, 上限はそれぞれ0.0, 1.0
        """
        feature = []

        moving = 0.0
        ex_x, ex_y = mouse[0]

        for coordinate in mouse:
            x, y = coordinate
            moving += ((x - ex_x)**2 + (y - ex_y)**2)**0.5
            ex_x, ex_y = x, y

        value = round(moving/100000 + len(click)/20, 2)
        if value > 1.0:
            value = 1.0
        feature.append(value)

        return feature

    def get_keyboard(self):
        try:
            return self.keyboard
        except NameError:
            return None

    def get_mouse(self):
        try:
            return self.mouse
        except NameError:
            return None

    def get_click(self):
        try:
            return self.click
        except NameError:
            return None

    def set_label(self, label):
        if label == "o":
            la = "work"
        else:
            la = "not work"
        return la
