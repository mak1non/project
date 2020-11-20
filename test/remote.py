import serial
import time


def main():
    with serial.Serial(port='/dev/ttyACM0', baudrate=115200) as arduino:
        time.sleep(1)

        while True:
            user_in = input('> ')

            if user_in == 'q':
                break
            elif user_in == 's':
                arduino.write(b'\x53')
            elif user_in == 'a':
                arduino.write(b'\x41')
            elif user_in == 'b':
                arduino.write(b'\x42')
            elif user_in == 'l':
                arduino.write(b'\x4c')
            elif user_in == 'r':
                arduino.write(b'\x52')

            arduino.flush()

        arduino.write(b'\x53')
        arduino.flush()


if __name__ == "__main__":
    main()
