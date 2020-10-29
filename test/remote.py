import serial


def main():
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

    while True:
        user_in = input('> ')

        if user_in == 'q':
            break

        serial_out = bytes(user_in, 'utf-8')
        ser.write(serial_out)

    ser.write(b'S')
    ser.close()


if __name__ == "__main__":
    main()