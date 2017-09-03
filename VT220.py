import serial
import io
import time


class VT220:
    ser = None  # raw serial connection, reference kept for cleanup
    sio = None  # buffered serial connection, this is internally used
    line_buffer = b''  # bytes string containing the current line up to (and containing) the newline char
    echo_characters = True  # when the user hits a key, should it display on the screen?

    def __init__(self, serial_port, baud_rate=9600, byte_size=serial.EIGHTBITS, stop_bits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE):
        if not serial_port:
            print('ERR! a valid serial port must be passed tp the constructor! use Util.serial_ports() to enumerate list of all found ports')
            exit(-1)
        if isinstance(serial_port, list):
            if len(serial_port) > 1:
                print('WARN! more than one serial port passed.  Blindly using first one...')
            if len(serial_port) is 0:
                print('ERR! no serial ports found on the computer! Exiting...')
                exit(-1)
            print('using port: ' + serial_port[0])
            port_name = serial_port[0]
        else:
            port_name = serial_port
        self.ser = serial.Serial(port=port_name, baudrate=baud_rate, bytesize=byte_size, parity=parity,
                                 stopbits=stop_bits, write_timeout=1, timeout=0)

        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1), newline=None, line_buffering=True)

    def __del__(self):
        self.ser.close()

    def clear_and_home(self):
        self.sio.write(bytes([27, 91, 50, 74, 27, 91, 72]))

    def light_on_dark(self):
        self.sio.write(bytes([0x9B, 0x3F, 0x35, 0x68]))

    def dark_on_light(self):
        self.sio.write(bytes([0x9B, 0x3F, 0x35, 0x6C]))

    def flash_screen(self, wait_time=0.03):
        self.light_on_dark()
        time.sleep(wait_time)
        self.dark_on_light()

    def write(self, text):
        self.sio.write(text.encode('ascii'))

    def read_char(self, block=False, on_char=None):
        if not block:
            char = self.sio.read(1)
        else:
            char = self.ser.read()

        if on_char:
            on_char(char)
        if self.echo_characters and char:
            self.write(char)
        return char

    def read_line(self, block=False, on_char=None, on_line=None):
        self.line_buffer = b''
        temp_buffer = self.read_char(block=block, on_char=on_char)
        self.line_buffer += temp_buffer
        while b'\n' not in temp_buffer:
            temp_buffer = self.read_char(block=block)
            if not block:
                time.sleep(0.1)  # prevent a busy loop
            self.line_buffer += temp_buffer
        return_var = self.line_buffer
        self.line_buffer = b''
        if on_line:
            on_line(return_var)
        return return_var

    def read_forever(self, on_char=None, on_line=None):
        if not on_char and not on_line:
            print('ERR! no callback functions passed!')
            return -1
        while True:
            self.read_line(block=True, on_char=on_char, on_line=on_line)
