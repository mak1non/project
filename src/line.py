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

    def detectLine(self, currentDirection=Direction.STOP, onlyShow=False):
        """線を認識する
        線が左右ブロックエリアに何 px 入っているのかをカウントし、
        それぞれ self.leftBlock と self.rightBlock に格納する

        Args:
            currentDirection (Direction, optional): 現在の進行方向 (デフォルト: Direction.STOP)

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
        self.binaryImg = cv2.adaptiveThreshold(grayImg, self.cfg.maxValue,
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY_INV,
                                               self.cfg.blockSize, self.cfg.c)
        if self.binaryImg is not None:
            # 中央ブロックエリアのフレームをセット
            centerBlock = self.binaryImg[0:self.cfg.trimH,
                                         (self.cfg.leftArea[1] +
                                          20):(self.cfg.rightArea[0] - 20)]
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
            self.detCB = cv2.countNonZero(centerBlock)
            # 左ブロックエリアの白ピクセルカウント
            self.detLB = cv2.countNonZero(leftBlock)
            # 右ブロックエリアの白ピクセルカウント
            self.detRB = cv2.countNonZero(rightBlock)

            direction = self.__dirSelect(currentDirection)
            return direction

        self.state = State.ERROR
        self.error = '画像の2値化失敗'
        return Direction.STOP

    def __dirSelect(self, currentDirection):
        """進行方向の決定

        Args:
            currentDirection (Direction): 現在の進行方向
        """
        # 各エリアの認識の有無
        # 念のため明示的にbool型にしている
        center = bool(self.detCB > 0)
        left = bool(self.detLB > 0)
        right = bool(self.detRB > 0)

        # 左右折時
        if currentDirection is Direction.LEFT:
            if left:
                return None
            elif center:
                # 中央
                return Direction.FORWARD
            elif right:
                # 右折
                return Direction.RIGHT
            return None
        elif currentDirection is Direction.RIGHT:
            if right:
                return None
            if center:
                # 中央
                return Direction.FORWARD
            elif left:
                # 左折
                return Direction.LEFT
            return None

        # 直進時
        if center and left and right:
            # 停止線
            self.state = State.STANDBY
            return Direction.STOP
        elif left:
            # 左に線が寄っている場合
            return Direction.LEFT
        elif right:
            # 右に線が寄っている場合
            return Direction.RIGHT
        elif center:
            # 中央
            # 線が見つからない時は、事前の状態を続けるため、この処理は動かない
            return Direction.FORWARD
        return None

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
            key = cv2.waitKey(35) & 0xFF

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
            saveTime = now.strftime('%Y-%m-%dT%H_%M_%S')

            # 写真の撮影
            cv2.imwrite('pictures/' + saveTime + '_orig.jpg', self.origImg)
            cv2.imwrite('pictures/' + saveTime + '_binary.jpg', self.binaryImg)

    def releaseCam(self):
        """カメラを閉じる
        """
        self.camera.release()
