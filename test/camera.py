import cv2
import sys


def main():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, img = camera.read()
        if ret is not True:
            sys.exit(1)

        cv2.imshow('Camera', img)
        key = cv2.waitKey(33) & 0xFF
        if key is ord('q') or key is ord('Q'):
            break


if __name__ == "__main__":
    main()
