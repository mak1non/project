#!/usr/bin/env python3

import cv2
import sys

# 二値化の閾値
threshold = 64
maxVal = 255

# トリミングサイズ
trimY = 180
trimH = 30

# 左ブロックエリア設定
leftXArea = (200, 210)
leftYArea = (0, trimH)

# 右ブロックエリア設定
rightXArea = (400, 410)
rightYArea = (0, trimH)

# カメラ取得
camera = cv2.VideoCapture(0)

# リサーブチェック
if camera.isOpened() is False:
    print("Can not open camera")
    sys.exit()


def detectLine():
    """線を認識する

    Returns:
        str: エラー箇所
        int: 左の白ピクセルカウント
        int: 右の白ピクセルカウント
    """
    # エラー箇所
    msg = ''

    # 画像を取得
    ret, frame = camera.read()
    if ret is True:
        frame = frame[trimY:trimY + trimH, ]  # 画像をトリミング
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # グレースケール化
    else:
        msg = "画像取得失敗"
        return msg, None, None

    # 画像の2値化
    ret, frame = cv2.threshold(frame, threshold, maxVal, cv2.THRESH_BINARY_INV)
    if ret:
        # 左ブロックエリア描画
        cv2.rectangle(frame,
                      (leftXArea[0], leftYArea[0]),
                      (leftXArea[1], leftYArea[1]),
                      (0, 0, 255),
                      1)
        # 右ブロックエリア描画
        cv2.rectangle(frame,
                      (rightXArea[0], rightYArea[0]),
                      (rightXArea[1], rightYArea[1]),
                      (0, 0, 255),
                      1)

        # 左ブロックエリアのフレームをセット
        leftBlock = frame[leftYArea[0]:leftYArea[1],
                          leftXArea[0]: leftXArea[1]]
        # 右ブロックエリアのフレームをセット
        rightBlock = frame[rightYArea[0]: rightYArea[1],
                           rightXArea[0]: rightXArea[1]]

        # 左ブロックエリアの白ピクセルカウント
        detLB = cv2.countNonZero(leftBlock)
        # 右ブロックエリアの白ピクセルカウント
        detRB = cv2.countNonZero(rightBlock)

        # 画面に表示
        cv2.imshow('Camera', frame)
    else:
        msg = "画像の2値化失敗"
        return msg, None, None

    return msg, detLB, detRB


def judgeLine(leftBlock, rightBlock):
    """線の状態を識別する

    Args:
        leftBlock (int): 左ブロックエリア
        rightBlock (int): 右ブロックエリア
    """
    if leftBlock > 0 and rightBlock > 0:
        print('Stop')
    elif leftBlock > 0:
        print('Left')
    elif rightBlock > 0:
        print('Right')
    else:
        print('Forward')


# 取得
while True:
    msg, detLB, detRB = detectLine()

    if msg == '':
        # 数値の表示
        print("detLB : " + str(detLB) + " detRB: " + str(detRB))

        judgeLine(detLB, detRB)
    else:
        # エラー表示
        print('エラー: ' + msg)
        break

    # 終了
    if cv2.waitKey(1) & 0xFF is ord('q'):
        break
