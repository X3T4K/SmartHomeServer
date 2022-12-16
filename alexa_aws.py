import urllib3
import os
import json
from alexa.skills.smarthome.alexa_response import AlexaResponse as AlexaResponseLight
from alexa.skills.smarthome.alexa_response_rollerShutter import AlexaResponse as AlexaResponseBlinds


def lambda_handler(request, context):
    # Dump the request for logging - check the CloudWatch logs
    print('lambda_handler request  -----')
    print(json.dumps(request))

    if context is not None:
        print('lambda_handler context  -----')

    # Validate we have an Alexa directive
    if 'directive' not in request:
        aer = AlexaResponseLight(
            name='ErrorResponse',
            payload={'type': 'INVALID_DIRECTIVE',
                     'message': 'Missing key: directive, Is the request a valid Alexa Directive?'})
        return send_response(aer.get())

    # Check the payload version
    payload_version = request['directive']['header']['payloadVersion']
    if payload_version != '3':
        aer = AlexaResponseLight(
            name='ErrorResponse',
            payload={'type': 'INTERNAL_ERROR',
                     'message': 'This skill only supports Smart Home API version 3'})
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request['directive']['header']['name']
    namespace = request['directive']['header']['namespace']

    # Handle the incoming request from Alexa based on the namespace

    if namespace == 'Alexa.Authorization':
        if name == 'AcceptGrant':
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request['directive']['payload']['grant']['code']
            grantee_token = request['directive']['payload']['grantee']['token']
            aar = AlexaResponseLight(namespace='Alexa.Authorization', name='AcceptGrant.Response')
            return send_response(aar.get())

    if namespace == 'Alexa.Discovery':
        # il discovery cambia ogni volta che c'è da dichiarare un nuovo oggetto
        if name == 'Discover':
            messageId = request['directive']['header']['messageId']
            jsontxt = '{ "event": { "header": { "namespace": "Alexa.Discovery", "name": "Discover.Response", "payloadVersion": "3", "messageId": "' + messageId + '" }, "payload": { "endpoints": [ { "endpointId": "sensor_temp_camera_502__225", "manufacturerName": "Generic PT100", "description": "Sensore di Temperatura camere", "friendlyName": "Temperatura camera", "displayCategories": ["TEMPERATURE_SENSOR"], "cookie": {}, "capabilities": [ { "type": "AlexaInterface", "interface": "Alexa.TemperatureSensor", "version": "3", "properties": { "supported": [ { "name": "temperature" } ], "proactivelyReported": true, "retrievable": true } }, { "type": "AlexaInterface", "interface": "Alexa", "version": "3" } ] } ]}}}'
            data = json.loads(jsontxt)
            return send_response(data)

    if namespace == 'Alexa.PowerController':
        # Note: l'id di scrittura è impostato nell'endpointID, accensione/spegnimento integrati nel JSON
        endpoint_id = request['directive']['endpoint']['endpointId']
        power_state_value = 'OFF' if name == 'TurnOff' else 'ON'
        correlation_token = request['directive']['header']['correlationToken']
        # Check for an error when setting the state
        state_set = set_coil_state(endpoint_id=endpoint_id, value=power_state_value)
        if not state_set:
            return AlexaResponseLight(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        apcr = AlexaResponseLight(correlation_token=correlation_token)
        apcr.add_context_property(namespace='Alexa.PowerController', name='powerState', value=power_state_value)
        return send_response(apcr.get())

    if namespace == 'Alexa.BrightnessController':
        # Note: endpoint di scrittura è sempre la word 139, la percentuale è trasformata in valore ed inviata
        endpoint_id = request['directive']['endpoint']['endpointId']
        percentage = request['directive']['payload']['brightness']
        correlation_token = request['directive']['header']['correlationToken']
        # Check for an error when setting the state
        register_value = calculate_percentage(Percentage=percentage)
        state_set = set_register_value(endpoint_id=139, value=register_value)
        if not state_set:
            return AlexaResponseLight(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        apcrb = AlexaResponseLight(correlation_token=correlation_token)
        apcrb.add_context_property(namespace='Alexa.BrightnessController', name='SetBrightness', value=percentage)
        return send_response(apcrb.get())

    if namespace == 'Alexa.TemperatureSensor':
        endpoint_id = request['directive']['endpoint']['endpointId']
        correlation_token = request['directive']['header']['correlationToken']
        messageid = request['event']['header']['messageId']
        alexa_response = temp_retriever(endpoint_temp=endpoint_id, messageId=messageid,
                                        correlationToken=correlation_token)
        if (alexa_response == NULL):
            return AlexaResponseLight(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        else:
            return send_response(alexa_response)

    if namespace == 'Alexa.ModeController':
        # Note: il position.UP restituisce errore per adesso perché nel plc non ci sono le istruzioni di alzata
        # l'EndPoint nel raspBerry corrisponde ad un array di coils da scrivere per muovere le tapparelle
        endpoint_id = request['directive']['endpoint']['endpointId']
        correlation_token = request['directive']['header']['correlationToken']
        movement = request['directive']['payload']['mode']
        state_set = False
        if 'zone' in str(endpoint_id):
            print('tapparelle')
            if 'Position.Up' in str(movement):
                return AlexaResponseLight(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
            # Check for an error when setting the state
            state_set = blinds_management(endpoint_id=endpoint_id, movement=movement)
        if 'garage' in str(endpoint_id):
            if 'Position.Down' in str(movement):
                return AlexaResponseLight(
                    name='ErrorResponse',
                    payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
            # Check for an error when setting the state
            state_set = garage_management(movement=movement)
        if not state_set:
            return AlexaResponseLight(
                name='ErrorResponse',
                payload={'type': 'ENDPOINT_UNREACHABLE', 'message': 'Unable to reach endpoint database.'}).get()
        apcrc = AlexaResponseLight(correlation_token=correlation_token)
        apcrc.add_context_property(namespace='Alexa.ModeController', name='SetMode', value=movement)
        return send_response(apcrc.get())


http_server = os.environ['HTTP_SERVER']


def send_response(response):
    # TODO Validate the response
    print('lambda_handler response -----')
    print(response)
    return response


def set_coil_state(endpoint_id, value):
    http = urllib3.PoolManager()
    url = http_server + "/coil/writer/" + endpoint_id + "/" + value
    return http.request('POST', url)


def calculate_percentage(Percentage):
    return ((3500 * Percentage / 100) + 500)


def set_register_value(endpoint_id, value):
    http = urllib3.PoolManager()
    url = http_server + "/register/writer/" + str(endpoint_id) + "/" + str(int(round(value)))
    print(url)
    http.request('POST', url)
    return True


def blinds_management(endpoint_id, movement):
    http = urllib3.PoolManager()
    url = http_server + "/coil/blinds_management/" + str(endpoint_id) + "/" + str(movement)
    http.request('POST', url)
    return True


def garage_management(movement):
    http = urllib3.PoolManager()
    url = http_server + "/coil/garage_management/" + str(movement)
    http.request('POST', url)
    return True


def temp_retriever(endpoint_temp, messageId, correlationToken):
    http = urllib3.PoolManager()
    url = http_server + "/register/reader/" + str(endpoint_temp)
    response = http.request('GET', url + ip)
    data = response.data
    values = json.loads(data)
    values['event']['endpoint']['endpointId'] = endpoint_temp
    values['event']['header']['messageId'] = messageId
    values['event']['header']['correlationToken'] = correlationToken
    return values
