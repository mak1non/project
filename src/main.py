#!/usr/bin/env python3

import sys
from car import Car
from line import Line


def main():
    # 取得
    line = Line()

    # カメラ取得チェック
    if line.camera.isOpened() is False:
        print("Can't open camera.")
        sys.exit(1)  # プログラム終了

    # モーター操作
    car = Car()

    try:
        while True:
            msg = line.detectLine()

            if msg == '':
                line.printDetect()

                # 線の判定
                car.judgeLine(line.detLB, line.detRB)
                car.run()
            else:
                # エラー表示
                print('エラー: ' + msg)
                break

    # Ctrl + C 押下時にメッセージを表示
    except KeyboardInterrupt:
        print('Keyboard interrupted')

    # 終了時にカメラを開放する
    finally:
        line.releaseCam()


# 直接起動時のみ処理を実行する
if __name__ == '__main__':
    main()
