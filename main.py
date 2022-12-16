# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pyModbusTCP.client import ModbusClient


def print_hi(name):
    c = ModbusClient(host="192.168.1.174", port=502, auto_open=True, auto_close=True)

    # temp_camera = c.read_holding_registers(502, 1)[0]/225
    # temp_salotto = c.read_holding_registers(503, 1)[0]/250
    # temp_mandata_aq = c.read_holding_registers(504, 1)[0]/240
    # print(temp_mandata_aq)
    messageId = 'x'
    json_txt = '{ "event": { "header": { "namespace": "Alexa.Discovery", "name": "Discover.Response", "payloadVersion": "3", "messageId": "' + messageId + '" }, "payload": { "endpoints": [ { "endpointId": "sensor_temp_camera_225", "manufacturerName": "Generic PT100", "description": "Sensore di Temperatura camere", "friendlyName": "Temperatura camera", "displayCategories": ["TEMPERATURE_SENSOR"], "cookie": {}, "capabilities": [ { "type": "AlexaInterface", "interface": "Alexa.TemperatureSensor", "version": "3", "properties": { "supported": [ { "name": "temperature" } ], "proactivelyReported": true, "retrievable": true } }, { "type": "AlexaInterface", "interface": "Alexa", "version": "3" } ] } ]}}}'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = "night-zone-2"
    if 'zone' in str(x):
        print_hi('PyCharm')
    else:
        print_hi("gg")
