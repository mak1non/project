import RPi.GPIO as GPIO
import time
from direction import Direction


class Car:
    def __init__(self):
        # 初期化
        self.direction = Direction.STOP

        # 出力ピン
        self.stopPin = 7  # 停止
        self.fwdPin = 8  # 前進
        self.backPin = 10  # 後退
        self.leftPin = 11  # 左折
        self.rightPin = 12  # 右折
        self.outputs = (self.stopPin, self.fwdPin, self.backPin, self.leftPin,
                        self.rightPin)

        # 出力の準備
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button, GPIO.IN)
        GPIO.setup(self.outputs, GPIO.OUT)

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

    def run(self):
        """Arduino に指示を出す
        """
        print(self.direction)
        GPIO.output(self.outputs, False)

        # 各種出力
        if self.direction == Direction.STOP:
            GPIO.output(self.stopPin, True)
        elif self.direction == Direction.FORWARD:
            GPIO.output(self.fwdPin, True)
        elif self.direction == Direction.BACKWARD:
            GPIO.output(self.backPin, True)
        elif self.direction == Direction.LEFT:
            GPIO.output(self.leftPin, True)
        elif self.direction == Direction.RIGHT:
            GPIO.output(self.rightPin, True)

        # 調整
        time.sleep(0.03)

    def dispose(self):
        """GPIO を手放す
        """
        print('GPIO Close')
        GPIO.cleanup()
