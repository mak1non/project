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
        sys.exit()

    # モーター操作
    car = Car()

    # Ctrl + C で終了時にカメラを開放する
    try:
        while True:
            msg, detLB, detRB = line.detectLine()

            if msg == '':
                # 数値の表示
                print("detLB : " + str(detLB) + " detRB: " + str(detRB))

                # 線の判定
                car.judgeLine(detLB, detRB)
                car.run()
            else:
                # エラー表示
                print('エラー: ' + msg)
                break

    except KeyboardInterrupt:
        line.releaseCam()


if __name__ == '__main__':
    main()
