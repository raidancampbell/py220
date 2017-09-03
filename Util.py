import sys
import glob
import serial


class Util:

    @staticmethod
    def serial_ports(ignore_bluetooth=True):
        if sys.platform.startswith('win'):  # windows COM port enumerations
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):  # linux and cygwin support
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):  # OSX support
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:  # for every possible port name
            try:
                s = serial.Serial(port)  # open it and close it
                s.close()
                print('found port: ' + str(port))
                if ignore_bluetooth and 'bluetooth' not in str(port).lower():
                    result.append(port)  # if nothing went wrong, the port exists on the system
                else:
                    print('port was bluetooth, and ignore_bluetooth flag was set. skipping.')
            except (OSError, serial.SerialException):  # if something went wrong, the port does not exist
                pass
        return result  # return the list of ports that currently actually exist on the system
