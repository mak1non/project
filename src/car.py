import serial
import time
from direction import Direction


class Car:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, wait=1):
        """Arduino に指示を出すクラス

        Args:
            port (str, optional): 出力先のシリアルポート (デフォルト: '/dev/ttyACM0')
            baud (int, optional): 通信間隔 (デフォルト: 115200)
            wait (int, optional): カーブ時の待ち時間 (デフォルト: 1)
        """
        # 初期化
        self.first = True
        self.preDirection = Direction.STOP

        # シリアル通信の設定値
        self.port = port
        self.baudrate = baudrate

        # カーブ時の待ち時間
        self.wait = wait

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

    def run(self, direction):
        """Arduino に指示を出す
        """
        if direction is None:
            return

        # 状態が変化していなければ出力しない
        if self.preDirection is direction:
            return

        # 各種出力
        if direction is Direction.STOP:
            self.arduino.write(b'\x53')  # 停止
        elif direction is Direction.FORWARD:
            self.arduino.write(b'\x41')  # 前進
        elif direction is Direction.BACKWARD:
            self.arduino.write(b'\x42')  # 後退
        elif self.first:
            self.first = False
            if direction is Direction.LEFT:
                time.sleep(self.wait)
                self.arduino.write(b'\x4c')  # 左折
            elif direction is Direction.RIGHT:
                time.sleep(self.wait)
                self.arduino.write(b'\x52')  # 右折
        else:
            if self.preDirection is Direction.STOP:
                return
            elif direction is Direction.LEFT:
                time.sleep(self.wait)
                self.arduino.write(b'\x4c')  # 左折
            elif direction is Direction.RIGHT:
                time.sleep(self.wait)
                self.arduino.write(b'\x52')  # 右折

        # 方向を表示
        print(direction)

        # 前の状態を保存する
        self.preDirection = direction
