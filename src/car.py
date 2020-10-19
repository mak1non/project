import time
from direction import Direction


class Car:
    def __init__(self):
        # 入力ピン
        self.button = 33

        # 出力ピン
        self.stopPin = 40
        self.fwdPin = 38
        self.backPin = 37
        self.leftPin = 36
        self.rightPin = 35
        self.outputs = (self.stopPin, self.fwdPin, self.backPin, self.leftPin,
                        self.rightPin)

        # 初期化
        self.direction = Direction.STOP

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
        """実際にモーターを動作させる
        """
        time.sleep(0.01)

        if self.direction == Direction.STOP:
            print("STOP")
        elif self.direction == Direction.FORWARD:
            print("FORWARD")
        elif self.direction == Direction.BACKWARD:
            print("BACKWARD")
        elif self.direction == Direction.LEFT:
            print("LEFT")
        elif self.direction == Direction.RIGHT:
            print("RIGHT")

    def dispose(self):
        """GPIO を手放す
        """
        print("GPIO dispose")
