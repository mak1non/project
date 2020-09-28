import cv2
import datetime
from config import Config
from state import State


class Line:

    def __init__(self):
        # 設定ファイル
        self.cfg = Config()

        # 状態
        self.state = State.NORMAL
        self.error = ''

        # カメラ取得
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # 初期化
        self.origImg = None
        self.binaryImg = None
        self.detLB = 0
        self.detRB = 0

    def detectLine(self):
        """線を認識する
        """

        # 画像を取得
        ret, self.origImg = self.camera.read()
        if ret is True:
            # 画像をトリミング
            trimImg = self.origImg[
                self.cfg.trimY:self.cfg.trimY +
                self.cfg.trimH,
            ]

            # グレースケール化
            grayImg = cv2.cvtColor(trimImg, cv2.COLOR_BGR2GRAY)
        else:
            self.state = State.ERROR
            self.error = '画像取得失敗'

        # 画像の2値化
        ret, self.binaryImg = cv2.threshold(
            grayImg,
            self.cfg.threshold,
            self.cfg.maxValue,
            cv2.THRESH_BINARY_INV
        )
        if ret:
            # 左ブロックエリアのフレームをセット
            leftBlock = self.binaryImg[
                0:self.cfg.trimH,
                self.cfg.leftArea[0]:self.cfg.leftArea[1]
            ]
            # 右ブロックエリアのフレームをセット
            rightBlock = self.binaryImg[
                0:self.cfg.trimH,
                self.cfg.rightArea[0]:self.cfg.rightArea[1]
            ]

            # 左ブロックエリアの白ピクセルカウント
            self.detLB = cv2.countNonZero(leftBlock)
            # 右ブロックエリアの白ピクセルカウント
            self.detRB = cv2.countNonZero(rightBlock)

        else:
            self.state = State.ERROR
            self.error = '画像の2値化失敗'

    def showImg(self):
        """画像の表示
        """
        # showImg() より前に呼ばれたらエラーを表示する
        if self.origImg is None or self.binaryImg is None:
            print('エラー: 画像が撮影されていません')
            return

        # 左ブロックエリア描画
        cv2.rectangle(
            self.binaryImg,
            (self.cfg.leftArea[0], 0),
            (self.cfg.leftArea[1], self.cfg.trimH),
            (0, 0, 255),
            1
        )
        # 右ブロックエリア描画
        cv2.rectangle(
            self.binaryImg,
            (self.cfg.rightArea[0], 0),
            (self.cfg.rightArea[1], self.cfg.trimH),
            (0, 0, 255),
            1
        )

        # 画面に表示
        cv2.imshow('Camera', self.origImg)
        cv2.imshow('Sensor', self.binaryImg)

        # 1000ms / 30fps (Camera) = 33.3(...)
        key = cv2.waitKey(33) & 0xFF

        if key is ord('s') or key is ord('S'):
            now = datetime.datetime.now()
            time = now.strftime("%Y-%m-%dT%H_%M_%S")
            cv2.imwrite('pictures/' + time + '_orig.jpg', self.origImg)
            cv2.imwrite('pictures/' + time + '_binary.jpg', self.binaryImg)
        elif key is ord('q') or key is ord('Q'):
            self.state = State.EXIT

    def printDetect(self):
        """カメラの認識値を表示する (テスト用)
        """
        print(
            "detLB : " + str(self.detLB) +
            " detRB: " + str(self.detRB)
        )

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
