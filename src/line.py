import cv2
import datetime
from config import Config
from direction import Direction
from state import State


class Line:
    def __init__(self):
        # 設定ファイル
        self.cfg = Config()

        # 状態
        self.state = State.STANDBY
        self.error = ''

        # カメラ取得
        self.camera = cv2.VideoCapture(self.cfg.cIndex)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # 初期化
        self.origImg = None
        self.binaryImg = None

    def detectLine(self, onlyShow=False):
        """線を認識する
        線が左右ブロックエリアに何 px 入っているのかをカウントし、
        それぞれ self.leftBlock と self.rightBlock に格納する

        Args:
            onlyShow (bool, optional): 撮影のみ行う (デフォルト: False)

        Returns:
            Direction: 進行方向
        """
        # 白黒画像
        grayImg = None

        # 画像を取得
        ret, self.origImg = self.camera.read()
        if ret is not True:
            self.state = State.ERROR
            self.error = '画像取得失敗'
            return Direction.STOP

        # 画像をトリミング
        trimImg = self.origImg[self.cfg.trimY:self.cfg.trimY +
                               self.cfg.trimH, ]

        # グレースケール化
        grayImg = cv2.cvtColor(trimImg, cv2.COLOR_BGR2GRAY)

        # 画像の2値化
        ret, self.binaryImg = cv2.threshold(grayImg, self.cfg.threshold,
                                            self.cfg.maxValue,
                                            cv2.THRESH_BINARY_INV)
        if ret:
            # 中央ブロックエリアのフレームをセット
            centerBlock = self.binaryImg[
                0:self.cfg.trimH, self.cfg.leftArea[1]:self.cfg.rightArea[0]]
            # 左ブロックエリアのフレームをセット
            leftBlock = self.binaryImg[
                0:self.cfg.trimH, self.cfg.leftArea[0]:self.cfg.leftArea[1]]
            # 右ブロックエリアのフレームをセット
            rightBlock = self.binaryImg[
                0:self.cfg.trimH, self.cfg.rightArea[0]:self.cfg.rightArea[1]]

            # 撮影のみの場合はカウントはしない
            if onlyShow:
                return Direction.STOP

            # 中央ブロックエリアの白ピクセルカウント
            detCB = cv2.countNonZero(centerBlock)
            # 左ブロックエリアの白ピクセルカウント
            detLB = cv2.countNonZero(leftBlock)
            # 右ブロックエリアの白ピクセルカウント
            detRB = cv2.countNonZero(rightBlock)

            direction = self.__dirSelect(detCB, detLB, detRB)
            return direction

        self.state = State.ERROR
        self.error = '画像の2値化失敗'
        return Direction.STOP

    def __dirSelect(self, centerBlock, leftBlock, rightBlock):
        """進行方向の決定

        Args:
            centerBlock (int): 中央ブロックエリアの白ピクセル数
            leftBlock (int): 左ブロックエリアの白ピクセル数
            rightBlock (int): 右ブロックエリアの白ピクセル数
        """
        if centerBlock > 0 and leftBlock > 0 and rightBlock > 0:
            # 停止線
            self.state = State.STANDBY
            return Direction.STOP
        elif leftBlock > 0:
            # 左に線が寄っている場合
            return Direction.LEFT
        elif rightBlock > 0:
            # 右に線が寄っている場合
            return Direction.RIGHT
        elif centerBlock > 0:
            # 中央
            # 線が見つからない時は、事前の状態を続けるため、この処理は動かない
            return Direction.FORWARD

    def imgCheck(self):
        """detectLine() より前に呼ばれたらエラーを表示する

        Returns:
            bool: 画像の存在の有無
        """
        if self.origImg is None or self.binaryImg is None:
            self.state = State.ERROR
            self.error = '画像が撮影されていません'
            return False
        else:
            return True

    def showImg(self):
        """画像の表示
        """
        if self.imgCheck():
            # 左ブロックエリア描画
            cv2.rectangle(self.binaryImg, (self.cfg.leftArea[0], 0),
                          (self.cfg.leftArea[1], self.cfg.trimH), (0, 0, 255),
                          1)
            # 右ブロックエリア描画
            cv2.rectangle(self.binaryImg, (self.cfg.rightArea[0], 0),
                          (self.cfg.rightArea[1], self.cfg.trimH), (0, 0, 255),
                          1)

            # 画面に表示
            cv2.imshow('Camera', self.origImg)
            cv2.imshow('Sensor', self.binaryImg)

            # 1000ms / 30fps (Camera) = 33.3(...)
            key = cv2.waitKey(30) & 0xFF

            # キーの判別
            if key is ord('a') or key is ord('A'):
                # 開始
                self.state = State.NORMAL
            elif key is ord('s') or key is ord('S'):
                # 停止
                self.state = State.STANDBY
            elif key is ord('p') or key is ord('P'):
                # 画像の保存
                self.saveImg()
            elif key is ord('q') or key is ord('Q'):
                # 終了
                self.state = State.EXIT

    def saveImg(self):
        """画像の保存
        """
        # detectLine() より前に呼ばれたらエラーを表示する
        if self.imgCheck():
            # 時間の取得
            now = datetime.datetime.now()
            time = now.strftime('%Y-%m-%dT%H_%M_%S')

            # 写真の撮影
            cv2.imwrite('pictures/' + time + '_orig.jpg', self.origImg)
            cv2.imwrite('pictures/' + time + '_binary.jpg', self.binaryImg)

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
