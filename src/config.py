import configparser


class Config:
    def __init__(self, config='config.ini'):
        """設定ファイルの読み込み

        Args:
            config (str, optional): 設定ファイルのファイル名 (デフォルト: 'config.ini')
        """
        # 設定ファイルの読み込み
        config_ini = configparser.SafeConfigParser()
        config_ini.read(config, encoding='utf-8')

        # テスト用
        config_test = config_ini['DEFAULT']

        # 設定ファイル未存在時の処理
        if config_test.get('version') != '3':
            print('注意: 設定ファイルが存在しません。新規作成します。')
            self.__writeDefault()
        else:
            self.__readConfig(config_ini)

    def __writeDefault(self):
        """デフォルト設定の書き込み
        """
        config = configparser.SafeConfigParser()

        # テスト用
        config['DEFAULT'] = {'version': 3}

        # カメラ番号
        config['camera'] = {'index': 0}

        # 2値化の設定
        config['binary'] = {'block_size': 15, 'c': 7, 'max_value': 255}

        # トリミングサイズ
        config['trim'] = {'y_coordinate': 420, 'height': 50}

        # 左右ブロックエリア
        config['area'] = {
            'l_start': 40,
            'l_end': 130,
            'r_start': 410,
            'r_end': 500
        }

        # カーブ時の待ち時間
        config['turn'] = {'wait': 1}

        # 設定の書き込み
        with open('config.ini', 'w') as file:
            config.write(file)

        self.__readConfig(config)

    def __readConfig(self, config):
        """設定の読み込み

        Args:
            config (SafeConfigParser): 設定オブジェクト
        """
        # カメラ番号
        self.cIndex = int(config['camera']['index'])

        # 2値化の設定
        self.blockSize = int(config['binary']['block_size'])
        self.c = int(config['binary']['c'])
        self.maxValue = int(config['binary']['max_value'])

        # トリミングサイズ
        self.trimY = int(config['trim']['y_coordinate'])
        self.trimH = int(config['trim']['height'])

        # 左右ブロックエリア
        self.leftArea = (int(config['area']['l_start']),
                         int(config['area']['l_end']))
        self.rightArea = (int(config['area']['r_start']),
                          int(config['area']['r_end']))

        # カーブ時の待つ時間
        self.turn_wait = float(config['turn']['wait'])
