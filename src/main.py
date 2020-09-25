#!/usr/bin/env python3

import sys
from car import Car
from line import Line
from state import State


def main():
    print("""
=== 操作方法 ===
[q]: 終了
""")

    # 取得
    line = Line()

    # カメラ取得チェック
    if line.camera.isOpened() is False:
        print("Can't open camera.")
        sys.exit(1)  # プログラム終了

    # モーター操作
    car = Car()

    try:
        while line.state is State.NORMAL:
            # 線の認識
            line.detectLine()
            line.showImg()
            line.printDetect()

            # 判定
            car.judgeLine(line.detLB, line.detRB)
            car.run()

        if line.state is State.ERROR:
            print('エラー: ' + line.error)
        elif line.state is State.EXIT:
            print('終了')

    # Ctrl + C 押下時にメッセージを表示
    except KeyboardInterrupt:
        print('Keyboard interrupted')

    # 終了時にカメラを開放する
    finally:
        line.releaseCam()


# 直接起動時のみ処理を実行する
if __name__ == '__main__':
    main()
