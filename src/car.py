import serial
import time
from direction import Direction


class Car:
    def __init__(self, port='/dev/ttyACM0', baud='9600'):
        # 初期化
        self.direction = Direction.STOP

        # シリアル通信の準備
        self.serial = serial.Serial(port, baud)

    def judgeLine(self, leftBlock, rightBlock):
        """線に合わせて進行方向を変える
        
        Args:
            leftBlock (int): 左ブロックエリア
            rightBlock (int): 右ブロックエリア
        """
        if leftBlock > 0 and rightBlock > 0:
            self.direction = Direction.STOP
        elif leftBlock > 0:
            self.direction = Direction.LEFT
        elif rightBlock > 0:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.FORWARD

    def run(self, line):
        """Arduino に指示を出す

        Args:
            line (Line): Line クラスのインスタンス
        """
        time.sleep(0.01)

        if self.direction == Direction.STOP:
            print('STOP')
            self.serial.write(int.to_bytes(0, 1, 'big'))
        elif self.direction == Direction.FORWARD:
            print('FORWARD')
            self.serial.write(int.to_bytes(1, 1, 'big'))
        elif self.direction == Direction.BACKWARD:
            print('BACKWARD')
            self.serial.write(int.to_bytes(2, 1, 'big'))
        elif self.direction == Direction.LEFT:
            print('LEFT')
            self.serial.write(int.to_bytes(3, 1, 'big'))
        elif self.direction == Direction.RIGHT:
            print('RIGHT')
            self.serial.write(int.to_bytes(4, 1, 'big'))

    def dispose(self):
        """シリアル通信を手放す
        """
        print('Stop')
        self.serial.write(0)

        print('Serial dispose')
        self.serial.close()
