import configparser


class Config:
    def __init__(self):
        # 設定ファイルの読み込み
        config_ini = configparser.SafeConfigParser()
        config_ini.read('config.ini', encoding='utf-8')

        # テスト用
        config_test = config_ini['DEFAULT']

        # 設定ファイル未存在時の処理
        if config_test.get('test') is None:
            print('注意: 設定ファイルが存在しません。新規作成します。')
            self.__writeDefault()
        else:
            self.__readConfig(config_ini)

    def __writeDefault(self):
        """デフォルト設定の書き込み
        """
        config = configparser.SafeConfigParser()

        # テスト用
        config['DEFAULT'] = {
            'test': True
        }

        # 2値化の設定
        config['binary'] = {
            'threshold': 64,
            'maxValue': 255
        }

        # トリミングサイズ
        config['trim'] = {
            'y_coordinate': 180,
            'height': 30
        }

        # 左右ブロックエリア
        config['area'] = {
            'L_start': 200,
            'L_end': 210,
            'R_start': 400,
            'R_end': 410
        }

        # 設定の書き込み
        with open('config.ini', 'w') as file:
            config.write(file)

        self.__readConfig(config)

    def __readConfig(self, config):
        """設定の読み込み

        Args:
            config (SafeConfigParser): 設定オブジェクト
        """
        # 2値化の設定
        cfg = config['binary']
        self.threshold = cfg.get('threshold')
        self.maxValue = cfg.get('maxValue')

        # トリミングサイズ
        cfg = config['trim']
        self.trimY = cfg.get('y_coordinate')
        self.trimH = cfg.get('height')

        # 左右ブロックエリア
        cfg = config['area']
        self.leftArea = (cfg.get('L_start'), cfg.get('L_end'))
        self.rightArea = (cfg.get('R_start'), cfg.get('R_end'))
