#!/usr/bin/env python3

import os
import time
from concurrent.futures import ThreadPoolExecutor
from car import Car
from config import Config
from direction import Direction
from line import Line
from state import State


def main():
    # 画像保存ディレクトリ作成
    os.makedirs('pictures/', mode=0o755, exist_ok=True)

    # 設定の取得
    config = Config()

    # カメラの取得
    line = Line(config)

    # カメラ取得チェック
    if line.camera.isOpened() is False:
        print("Can't open camera.")
        return

    # モーター操作の準備
    with Car() as car:
        print("\n--- 操作方法 ---\n[A]: 開始\n[S]: 一時停止\n[P]: 画像撮影\n[Q]: 終了\n")

        # シリアル通信の準備を待つ
        time.sleep(2)

        # シリアル通信は並列で行う
        with ThreadPoolExecutor(max_workers=1) as executor:
            while True:
                if line.state is State.STANDBY:
                    # 車両に停止状態を伝える
                    car.first = True

                    # 表示のみ
                    line.detectLine(onlyShow=True)
                    line.showImg()

                    # 停止
                    executor.submit(car.run, Direction.STOP)
                elif line.state is State.NORMAL:
                    # 線の認識
                    direction = line.detectLine(
                        currentDirection=car.preDirection)
                    line.showImg()

                    # 判定
                    executor.submit(car.run, direction)
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
