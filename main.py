# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pyModbusTCP.client import ModbusClient


def print_hi(name):
    c = ModbusClient(host="192.168.1.174", port=502, auto_open=True, auto_close=True)

    #temp_camera = c.read_holding_registers(502, 1)[0]/225
    #temp_salotto = c.read_holding_registers(503, 1)[0]/250
    temp_mandata_aq = c.read_holding_registers(504, 1)[0]/240
    print(temp_mandata_aq)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
