import serial


def main():
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

    while True:
        user_in = input('> ')

        if user_in == 'q':
            break

        serial_out = bytes(user_in, 'utf-8')
        arduino.write(serial_out)
        arduino.flush()

    arduino.write(b'S')
    arduino.flush()
    arduino.close()


if __name__ == "__main__":
    main()
