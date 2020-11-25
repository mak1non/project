#!/usr/bin/env python3

import os
import time
from car import Car
from line import Line
from state import State


def main():
    # 画像保存ディレクトリ作成
    os.makedirs('pictures/', mode=0o755, exist_ok=True)

    # カメラの取得
    line = Line()

    # カメラ取得チェック
    if line.camera.isOpened() is False:
        print("Can't open camera.")
        return

    # モーター操作の準備
    with Car() as car:
        print("\n--- 操作方法 ---\n[A]: 開始\n[S]: 画像撮影\n[Q]: 終了")

        # シリアル通信の準備を待つ
        time.sleep(2)

        while line.state is State.STANDBY:
            # 表示のみ
            line.detectLine(onlyShow=True)
            line.showImg()

        while line.state is State.NORMAL:
            # 線の認識
            detCB, detLB, detRB = line.detectLine()
            line.showImg()

            # 判定
            car.judgeLine(detCB, detLB, detRB)
            car.run()

        # エラー時の表示
        if line.state is State.ERROR:
            print('エラー: ' + line.error)
        elif line.state is State.EXIT:
            print('終了')

    # カメラを閉じる
    line.releaseCam()


# 直接起動時のみ処理を実行する
if __name__ == '__main__':
    main()
