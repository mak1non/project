#!/usr/bin/env python3

import sys
import line
import wheel


def main():
    # 取得
    cam = line.LineHandler()

    # カメラ取得チェック
    if cam.camera.isOpened() is False:
        print("Can't open camera.")
        sys.exit()

    # モーター操作
    car = wheel.MortarHandler()

    try:
        while True:
            msg, detLB, detRB = line.detectLine()

            if msg == '':
                # 数値の表示
                print("detLB : " + str(detLB) + " detRB: " + str(detRB))

                # 線の判定
                car.judgeLine(detLB, detRB)
                print(car.direction)
            else:
                # エラー表示
                print('エラー: ' + msg)
                break

    except KeyboardInterrupt:
        cam.dispose()


if __name__ == '__main__':
    main()
