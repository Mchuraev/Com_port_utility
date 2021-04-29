# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import serial
import multiprocessing as mp
import keyboard


def com_uart(port, baudrate, file_name, out) -> None:
    """
    :param port: address or com port number
    :param baudrate: speed com port
    :param file_name: log file name
    :param out: on/off console output
    :return: None
    """
    try:
        ser = serial.Serial()
        ser.baudrate = baudrate
        ser.port = port
        ser.close()
        ser.open()

        with open(f'{file_name}', 'w') as f:
            while flag.value == 1:
                strg = str(ser.readline()).strip(r"\n'").strip(r'\r').lstrip("b'")
                timest = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                writers = f'{timest}   {strg}\n'
                f.write(writers)
                if out == 'on':
                    print(f'{timest}   {strg}')
            try:
                ser.close()
            except:
                print("Couldn't close serial port.")
    except:
        print(f"Can't open connect, check {port}")
        flag2.value = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    opt = parser.add_argument
    opt('-p', '--port', help='address or com port number, default "/dev/ttyUSB0"')
    opt('-s', '--speed', help='speed com port, default 115200')
    opt('-l', '--log', help='log file name, default uart_log_{datetime}.log')
    opt('-o', '--output', help='on/off console output')
    args = parser.parse_args()
    time_log = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    port = args.port if args.port is not None else "/dev/ttyUSB0"
    speed = args.speed if args.speed is not None else 115200
    log = args.log if args.log is not None else f'uart_log_{time_log}.log'
    out = args.output if args.output is not None else 'on'

    flag = mp.Value('i', 1)
    flag2 = mp.Value('i', 1)

    com = mp.Process(target=com_uart, args=(port, speed, log, out))
    com.start()

    print('To stop the program, press <Ctrl+D> or <Ctrl+C> for ssh_session')
    key = 'ctrl+D'

    while True:
        if keyboard.is_pressed(key):
            flag.value = 0
            break
        if flag2.value == 0:
            break

    if flag.value == 0:
        com.terminate()
        com.join(timeout=1.0)
        com.close()
