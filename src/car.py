import serial
from direction import Direction


class Car:
    def __init__(self, port='/dev/ttyACM0', baud=115200):
        """Arduino に指示を出すクラス

        Args:
            port (str, optional): 出力先のシリアルポート (デフォルト: '/dev/ttyACM0')
            baud (int, optional): 通信間隔 (デフォルト: 115200)
        """
        # 初期化
        self.preDirection = Direction.STOP
        self.direction = Direction.STOP

        # シリアル通信の準備
        self.arduino = serial.Serial(port=port, baudrate=baud)

    def judgeLine(self, leftBlock, rightBlock):
        """線に合わせて進行方向を変える (line.py も参照)
        
        Args:
            leftBlock (int): 左ブロックエリアの白 px 数
            rightBlock (int): 右ブロックエリアの白 px 数
        """
        # 前の状態を保存する
        self.preDirection = self.direction

        if leftBlock > 0 and rightBlock > 0:
            # 左右どちらも線がある場合
            self.direction = Direction.STOP
        elif leftBlock > 0:
            # 左に線が寄っている場合
            self.direction = Direction.LEFT
        elif rightBlock > 0:
            # 右に線が寄っている場合
            self.direction = Direction.RIGHT
        else:
            # 何も無い場合
            self.direction = Direction.FORWARD

    def run(self):
        """Arduino に指示を出す
        """
        # 状態が変化していなければ出力しない
        if self.preDirection is self.direction:
            return

        # 方向を表示
        print(self.direction)

        # 各種出力
        if self.direction is Direction.STOP:
            self.arduino.write(b'S')  # 停止
        elif self.direction is Direction.FORWARD:
            self.arduino.write(b'A')  # 前進
        elif self.direction is Direction.BACKWARD:
            self.arduino.write(b'B')  # 後退
        elif self.direction is Direction.LEFT:
            self.arduino.write(b'L')  # 左折
        elif self.direction is Direction.RIGHT:
            self.arduino.write(b'R')  # 右折

        # 待つ
        self.arduino.flush()

    def dispose(self):
        """シリアル通信を終了する
        """
        # ブレーキする
        self.arduino.write(b'S')
        self.arduino.flush()

        # 終了する
        print('Serial Close')
        self.arduino.close()
