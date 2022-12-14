from datetime import datetime
import json
from flask import Flask, request, redirect
from flask import jsonify
from pyModbusTCP.client import ModbusClient
import re
import time

app = Flask(__name__)
c = ModbusClient(host="192.168.1.174", port=502, auto_open=True, auto_close=True)
lightCoilAddress = [97, 98, 93, 91, 90, 92, 95, 94, 96]
lightFriendlyName = ["corridoio", "salotto", "cucina", "camera da letto", "camera di ceci", "camera di Nik",
                     "Bagno blu", "bagno verde", "mansarda"]


@app.route("/coil/writer/<string:coil>/<string:value>", methods=['POST'])
def coil_writer(coil, value):
    value_available = re.findall(r'\d+', coil)
    coil_addr = (int(value_available[0]))
    value = True if value == "ON" else False
    is_ok = c.write_single_coil(coil_addr, value)
    return str(is_ok)


@app.route("/coil/reader/<string:coil>", methods=['GET'])
def coil_reader(coil):
    coil_addr = (int(coil))
    request = c.read_coils(coil_addr, 1)
    return str(request)


@app.route("/register/writer/<string:register>/<string:value>", methods=['POST'])
def holding_register_writer(register, value):
    register_addr = (int(register))
    value_addr = (int(value))
    request = c.write_single_register(register_addr, value_addr)
    return str(request)


@app.route("/register/reader/<string:address>", methods=['GET'])
def holding_register_reader(address):
    register_addr = (int(address))
    request = c.read_holding_registers(register_addr, 1)[0]
    return str(request)  # test the expected value


def build_blinds_array():
    # create a multidimensional array, first level: blinds in general, second level: zone, third level: if up or
    # down. and then the array to write
    all_up = []
    all_down = [1, 2, 3, 4, 6, 7, 8, 9]
    all_blinds = [all_down, all_up]
    day_up = []
    day_down = [1, 2, 3, 4]
    day_zone_blinds = [day_down, day_up]
    night_up = []
    night_down = [6, 7, 8, 9]
    night_zone_blinds = [night_down, night_up]
    global blinds_management_array
    blinds_management_array = [all_blinds, day_zone_blinds, night_zone_blinds]


@app.route("/coil/blinds_management/<string:zone>/<string:movement>", methods=['POST'])
def blinds_management(zone, movement):
    zone = (re.findall(r'\d+', zone))[0]
    movement = 1 if movement == "Position.Up" else 0
    coils_to_set = [blinds_management_array[int(zone)][movement]]
    return True
    # try:
    #    return True
    # finally:
    #    for coil in coils_to_set[0]:
    #        c.write_single_coil(int(coil), True)
    #       time.sleep(30)


@app.route("/coil/garage_management/<string:movement>", methods=['POST'])
def garage_management(movement):
    # movement = 1 if movement == "Position.Up" else 0
    movement = 1
    try:
        return True
    finally:
        c.write_single_coil(105, movement)


@app.route("/plc_sensor_retriever/<string:device_endpoint>", methods=['GET'])
def plc_sensor_retriever(device_endpoint):
    print(device_endpoint)
    end_point = device_endpoint.split('_')
    register_addr = int(end_point[3])
    correction_factor = int(end_point[4])
    temperature = c.read_holding_registers(register_addr, 1)[0] / correction_factor
    jsonstr_alexa_response = '{ "event": { "header": { "namespace": "Alexa", "name": "StateReport", "messageId": ' \
                             '"Unique identifier, preferably a version 4 UUID", "correlationToken": "Opaque ' \
                             'correlation token that matches the request", "payloadVersion": "3" }, "endpoint": { ' \
                             '"scope": { "type": "BearerToken", "token": "OAuth2.0 bearer token" }, "endpointId": ' \
                             '"endpoint ID", "cookie": {} }, "payload": { } }, "context": { "properties": [ { ' \
                             '"namespace": "Alexa.TemperatureSensor", "name": "temperature", "value": { "value": ' \
                             '19.9, "scale": "CELSIUS" }, "timeOfSample": "2017-02-03T16:20:50.52Z", ' \
                             '"uncertaintyInMilliseconds": 1000 } ] } } '
    json_alexa_response = json.loads(jsonstr_alexa_response)
    json_alexa_response['context']['properties'][0]['timeOfSample'] = time.strftime("%Y-%m-%dT%H:%M:%S.52Z")
    json_alexa_response['context']['properties'][0]['value']['value'] = int(temperature)
    return json.dumps(json_alexa_response)  # test the expected value


# @app.route("/light/google/<string:id>/<string:value>", methods=['POST'])
# def google_light_handler(id, value):
#    print('xxxxxxxx')
#    coil_towrite = 0
#    value = True if value == "ON" else False
#    for i in lightFriendlyName:
#        if fuzzy_search(lightFriendlyName[i], id):
#            coil_towrite = lightCoilAddress[i]
#            break
#    return coil_writer(coil_towrite, value)


# def fuzzy_search(Sequence, subSequence):
#    match_grade = fuzz.ratio(Sequence, subSequence)
#    if match_grade > 95:
#        return True
#    else:
#        return False

@app.route('/redirects')
def redirects():
    logAccess(str(request.remote_addr))
    return redirect("https://forms.gle/6Z6MehXEJeMpL7jx5")


@app.route('/returnLink/YUWhR%x5hQI(ig&W.Qw3y=a^mf(', methods=['GET'])
def returnLink():
    logAccess(str(request.remote_addr))
    # return ("https://drive.google.com/file/d/1-HwUgvn0hZnGowx9vj9K-5hmHUm3zAIf/view?usp=sharing")


def logAccess(ipAddress):
    f = open(r"/home/pi/Desktop/AccessLog.txt", "a")
    f.write("\n" + datetime.now().strftime("%Y-%m-%d %H:%M") + " " + str(ipAddress))
    f.close()


if __name__ == "__main__":
    build_blinds_array()
    app.run(host='192.168.1.10', debug=True)
