# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time

from flask import jsonify
from pyModbusTCP.client import ModbusClient

c = ModbusClient(host="192.168.1.174", port=502, auto_open=True, auto_close=True)


def print_hi(name):

    # temp_camera = c.read_holding_registers(502, 1)[0]/225
    # temp_salotto = c.read_holding_registers(503, 1)[0]/250
    # temp_mandata_aq = c.read_holding_registers(504, 1)[0]/240
    # print(temp_mandata_aq)
    messageId = 'x'
    json_txt = '{ "event": { "header": { "namespace": "Alexa.Discovery", "name": "Discover.Response", "payloadVersion": "3", "messageId": "' + messageId + '" }, "payload": { "endpoints": [ { "endpointId": "sensor_temp_camera_225", "manufacturerName": "Generic PT100", "description": "Sensore di Temperatura camere", "friendlyName": "Temperatura camera", "displayCategories": ["TEMPERATURE_SENSOR"], "cookie": {}, "capabilities": [ { "type": "AlexaInterface", "interface": "Alexa.TemperatureSensor", "version": "3", "properties": { "supported": [ { "name": "temperature" } ], "proactivelyReported": true, "retrievable": true } }, { "type": "AlexaInterface", "interface": "Alexa", "version": "3" } ] } ]}}}'


def plc_sensor_retriever(device_endpoint):
    # sensor_temp_camera_502_225
    end_point = device_endpoint.split('_')
    register_addr = (int(end_point[3]))
    correction_factor = (int(end_point[4]))
    temperature = (int(c.read_holding_registers(register_addr, 1)[0] / correction_factor))
    json_alexa_response = '{ "event": { "header": { "namespace": "Alexa", "name": "StateReport", "messageId": "Unique ' \
                          'identifier, preferably a version 4 UUID", "correlationToken": "Opaque correlation token ' \
                          'that matches the request", "payloadVersion": "3" }, "endpoint": { "endpointId": "endpoint ' \
                          'ID", "cookie": {} }, "payload": { } }, "context": { "properties": [ { "namespace": ' \
                          '"Alexa.TemperatureSensor", "name": "temperature", "value": { "value": 19.9, ' \
                          '"scale": "CELSIUS" }, "timeOfSample": "2017-02-03T16:20:50.52Z", ' \
                          '"uncertaintyInMilliseconds": 1000 } ] } } '
    json_alexa_response = jsonify(json_alexa_response)
    json_alexa_response['context']['properties']['timeOfSample'] = time.strftime("%Y-%m-%dT%H:%M:%S.52Z")
    json_alexa_response['context']['properties']['value']['value'] = temperature
    return str(json_alexa_response)  # test the expected value

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    plc_sensor_retriever('sensor_temp_camera_502_225')
