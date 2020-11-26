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
        print("\n--- 操作方法 ---\n[A]: 開始\n[S]: 一時停止\n[P]: 画像撮影\n[Q]: 終了\n")

        # シリアル通信の準備を待つ
        time.sleep(2)

        while True:
            if line.state is State.STANDBY:
                # 表示のみ
                line.detectLine(onlyShow=True)
                line.showImg()

                # 停止
                car.run(1, 1, 1)
            elif line.state is State.NORMAL:
                # 線の認識
                detCB, detLB, detRB = line.detectLine()
                line.showImg()

                # 判定
                car.run(detCB, detLB, detRB)
            elif line.state is State.ERROR:
                # エラー時の表示
                print('エラー: ' + line.error)
                break
            elif line.state is State.EXIT:
                print('終了')
                break

    # カメラを閉じる
    line.releaseCam()


# 直接起動時のみ処理を実行する
if __name__ == '__main__':
    main()
