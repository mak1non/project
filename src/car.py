import serial
import time
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
        self.serial = serial.Serial(port=port, baudrate=baud)

    def judgeLine(self, leftBlock, rightBlock):
        """線に合わせて進行方向を変える
        
        Args:
            leftBlock (int): 左ブロックエリア
            rightBlock (int): 右ブロックエリア
        """
        # 状態を保存する
        self.preDirection = self.direction

        if leftBlock > 0 and rightBlock > 0:
            self.direction = Direction.STOP
        elif leftBlock > 0:
            self.direction = Direction.LEFT
        elif rightBlock > 0:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.FORWARD

    def run(self):
        """Arduino に指示を出す
        """
        # 方向を表示
        print(self.direction)

        # 状態が変化していなければ出力しない
        if self.preDirection == self.direction:
            print('Same')
        else:
            # 各種出力
            if self.direction == Direction.STOP:
                self.serial.write(b'S')
            elif self.direction == Direction.FORWARD:
                self.serial.write(b'A')
            elif self.direction == Direction.BACKWARD:
                self.serial.write(b'B')
            elif self.direction == Direction.LEFT:
                self.serial.write(b'L')
                time.sleep(2)  # 調整
            elif self.direction == Direction.RIGHT:
                self.serial.write(b'R')
                time.sleep(2)  # 調整

        # 調整
        time.sleep(0.03)

    def dispose(self):
        """シリアル通信を手放す
        """
        # ブレーキする
        self.serial.write(b'S')

        # 手放す
        print('Serial Close')
        self.serial.close()
