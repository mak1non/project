import cv2

# 二値化の閾値
threshold = 64
maxVal = 255

# トリミングサイズ
trimY = 180
trimH = 30

# 左ブロックエリア設定
leftXArea = (200, 210)
leftYArea = (0, trimH)

# 右ブロックエリア設定
rightXArea = (400, 410)
rightYArea = (0, trimH)


class Line:

    def __init__(self):
        # カメラ取得
        self.camera = cv2.VideoCapture(0)

    # TODO: 余裕があれば表示部分は切り出したいね
    def detectLine(self):
        """線を認識する

        Returns:
            str: エラー箇所
        """
        # エラー箇所
        msg = ''

        # 画像を取得
        ret, frame = self.camera.read()
        if ret is True:
            frame = frame[trimY:trimY + trimH, ]  # 画像をトリミング
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # グレースケール化
        else:
            msg = "画像取得失敗"
            return msg

        # 画像の2値化
        ret, frame = cv2.threshold(
            frame, threshold, maxVal, cv2.THRESH_BINARY_INV)
        if ret:
            # 左ブロックエリア描画
            cv2.rectangle(frame,
                          (leftXArea[0], leftYArea[0]),
                          (leftXArea[1], leftYArea[1]),
                          (0, 0, 255),
                          1)
            # 右ブロックエリア描画
            cv2.rectangle(frame,
                          (rightXArea[0], rightYArea[0]),
                          (rightXArea[1], rightYArea[1]),
                          (0, 0, 255),
                          1)

            # 左ブロックエリアのフレームをセット
            leftBlock = frame[leftYArea[0]:leftYArea[1],
                              leftXArea[0]: leftXArea[1]]
            # 右ブロックエリアのフレームをセット
            rightBlock = frame[rightYArea[0]: rightYArea[1],
                               rightXArea[0]: rightXArea[1]]

            # 左ブロックエリアの白ピクセルカウント
            self.detLB = cv2.countNonZero(leftBlock)
            # 右ブロックエリアの白ピクセルカウント
            self.detRB = cv2.countNonZero(rightBlock)

            # 画面に表示
            cv2.imshow('Camera', frame)
        else:
            msg = "画像の2値化失敗"
            return msg

        return msg

    def printDetect(self):
        """カメラの認識値を表示する (テスト用)
        """
        print("detLB : " + str(self.detLB) +
              " detRB: " + str(self.detRB))

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
