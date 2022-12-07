from flask import Flask
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


@app.route("/register/reader/<string:register>", methods=['GET'])
def holding_register_reader(register):
    register_addr = (int(register))
    request = c.read_holding_registers(register_addr, 1)
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
    try:
        return True
    finally:
        for coil in coils_to_set[0]:
            c.write_single_coil(int(coil), True)
            time.sleep(30)


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


if __name__ == "__main__":
    build_blinds_array()
    app.run(host='192.168.1.10', debug=True)
