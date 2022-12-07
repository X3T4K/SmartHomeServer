from pyModbusTCP.client import ModbusClient
import re
import time
from datetime import datetime


c = ModbusClient(host="192.168.1.174", port=502, auto_open=True, auto_close=True)




def logPassword():
    f = open(r"C:\Users\fanin\Desktop\g.txt", "a")
    f.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M"))
    f.close()

logPassword()
