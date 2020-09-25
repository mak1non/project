import cv2
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
        cv2.imshow('Sensor', self.binaryImg)

        # 1000ms / 30fps (Camera) = 33.3(...)
        if cv2.waitKey(33) & 0xFF is ord('q'):
            self.state = State.EXIT

    def detectLine(self):
        """線を認識する
        """

        # 画像を取得
        ret, frame = self.camera.read()
        if ret is True:
            frame = frame[trimY:trimY + trimH, ]  # 画像をトリミング
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # グレースケール化
        else:
            self.error = "画像取得失敗"

        # 画像の2値化
        ret, self.binaryImg = cv2.threshold(
            frame, threshold, maxVal, cv2.THRESH_BINARY_INV)
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
            self.error = "画像の2値化失敗"

    def printDetect(self):
        """カメラの認識値を表示する (テスト用)
        """
        print("detLB : " + str(self.detLB) +
              " detRB: " + str(self.detRB))

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
