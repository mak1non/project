import serial
import time
from direction import Direction


class Car:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        """Arduino に指示を出すクラス

        Args:
            port (str, optional): 出力先のシリアルポート (デフォルト: '/dev/ttyACM0')
            baud (int, optional): 通信間隔 (デフォルト: 115200)
        """
        # 初期化
        self.preDirection = Direction.STOP
        self.direction = Direction.STOP

        # シリアル通信の設定値
        self.port = port
        self.baudrate = baudrate

    def __enter__(self):
        """シリアル通信の準備
        """
        self.arduino = serial.Serial(port=self.port, baudrate=self.baudrate)
        return self

    def __exit__(self, exc_type, exc_value, trace):
        """シリアル通信を終了する
        """
        print('Serial Close', exc_type, exc_value, trace)

        # ブレーキする
        self.arduino.write(b'\x53')
        self.arduino.flush()

        # 終了する
        self.arduino.close()
        return True

    def run(self, centerBlock, leftBlock, rightBlock):
        """線に合わせて走行する (line.py も参照)
        
        Args:
            centerBlock (int): 中央ブロックエリアの白 px 数
            leftBlock (int): 左ブロックエリアの白 px 数
            rightBlock (int): 右ブロックエリアの白 px 数
        """
        # 前の状態を保存する
        self.preDirection = self.direction

        if centerBlock > 0 and leftBlock > 0 and rightBlock > 0:
            # 中央
            self.direction = Direction.STOP
        elif leftBlock > 0:
            # 左に線が寄っている場合
            self.direction = Direction.LEFT
        elif rightBlock > 0:
            # 右に線が寄っている場合
            self.direction = Direction.RIGHT
        elif centerBlock > 0:
            # 中央
            # 線が見つからない時は、事前の状態を続けるため、この処理は動かない
            self.direction = Direction.FORWARD

        self.__send()

    def __send(self):
        """Arduino に指示を出す
        """
        # 状態が変化していなければ出力しない
        if self.preDirection is self.direction:
            return

        # 方向を表示
        print(self.direction)

        # 各種出力
        if self.direction is Direction.STOP:
            self.arduino.write(b'\x53')  # 停止
        elif self.direction is Direction.FORWARD:
            self.arduino.write(b'\x41')  # 前進
        elif self.direction is Direction.BACKWARD:
            self.arduino.write(b'\x42')  # 後退
        elif self.direction is Direction.LEFT:
            self.arduino.write(b'\x53')  # 停止
            time.sleep(1)
            self.arduino.write(b'\x4c')  # 左折
        elif self.direction is Direction.RIGHT:
            self.arduino.write(b'\x53')  # 停止
            time.sleep(1)
            self.arduino.write(b'\x52')  # 右折

        # 待つ
        self.arduino.flush()
