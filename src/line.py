import cv2
import datetime
from state import State

# 二値化の閾値
threshold = 64
maxVal = 255

# トリミングサイズ
trimY = 180  # 縦座標
trimH = 30   # 高さ

# 左ブロックエリア設定
leftXArea = (200, 210)  # 始点, 終点
leftYArea = (0, trimH)

# 右ブロックエリア設定
rightXArea = (400, 410)
rightYArea = (0, trimH)


class Line:

    def __init__(self):
        # 状態
        self.state = State.NORMAL

        # カメラ取得
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def detectLine(self):
        """線を認識する
        """

        # 画像を取得
        ret, self.origImg = self.camera.read()
        if ret is True:
            trimImg = self.origImg[trimY:trimY + trimH, ]  # 画像をトリミング
            grayImg = cv2.cvtColor(
                trimImg, cv2.COLOR_BGR2GRAY)  # グレースケール化
        else:
            self.state = State.ERROR
            self.error = '画像取得失敗'

        # 画像の2値化
        ret, self.binaryImg = cv2.threshold(
            grayImg, threshold, maxVal, cv2.THRESH_BINARY_INV)
        if ret:
            # 左ブロックエリアのフレームをセット
            leftBlock = self.binaryImg[leftYArea[0]:leftYArea[1],
                                       leftXArea[0]: leftXArea[1]]
            # 右ブロックエリアのフレームをセット
            rightBlock = self.binaryImg[rightYArea[0]: rightYArea[1],
                                        rightXArea[0]: rightXArea[1]]

            # 左ブロックエリアの白ピクセルカウント
            self.detLB = cv2.countNonZero(leftBlock)
            # 右ブロックエリアの白ピクセルカウント
            self.detRB = cv2.countNonZero(rightBlock)

        else:
            self.state = State.ERROR
            self.error = '画像の2値化失敗'

    def showImg(self):
        # 左ブロックエリア描画
        cv2.rectangle(self.binaryImg,
                      (leftXArea[0], leftYArea[0]),
                      (leftXArea[1], leftYArea[1]),
                      (0, 0, 255),
                      1)
        # 右ブロックエリア描画
        cv2.rectangle(self.binaryImg,
                      (rightXArea[0], rightYArea[0]),
                      (rightXArea[1], rightYArea[1]),
                      (0, 0, 255),
                      1)

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
        print("detLB : " + str(self.detLB) +
              " detRB: " + str(self.detRB))

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
