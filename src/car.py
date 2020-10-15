import time

import RPi.GPIO as GPIO

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

        # 出力の準備
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button, GPIO.IN)
        GPIO.setup(self.outputs, GPIO.OUT)

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
        print(self.direction)
        GPIO.output(self.outputs, False)
        time.sleep(0.01)

        if GPIO.input(self.button) != 1:
            line.saveImg()

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

    def dispose(self):
        """GPIO を手放す
        """
        GPIO.cleanup()
