# Python program to demonstrate
# Conversion of JSON data to
# dictionary


# importing the module
import json

# Opening JSON file
messageId = 'meeeeeeeeeeeeeeeeee'
jsontxt = '{ "event": { "header": { "namespace": "Alexa.Discovery", "name": "Discover.Response", "payloadVersion": ' \
          '"3", "messageId": "'+ messageId + '" }, "payload": { "endpoints": [ { "endpointId": "<unique ID of the ' \
          'endpoint>", "manufacturerName": "<manufacturer name>", "description": "<Smart Blinds by Manufacturer>", ' \
          '"friendlyName": "<Blinds>", "displayCategories": ["INTERIOR_BLIND"], "cookie": {}, "capabilities": [ { ' \
          '"type": "AlexaInterface", "interface": "Alexa.ModeController", "instance": "Blinds.Position", "version": ' \
          '"3", "properties": { "supported": [ { "name": "mode" } ], "retrievable": true, "proactivelyReported": true ' \
          '}, "capabilityResources": { "friendlyNames": [ { "@type": "asset", "value": { "assetId": ' \
          '"Alexa.Setting.Opening" } } ] }, "configuration": { "ordered": false, "supportedModes": [ { "value": ' \
          '"Position.Up", "modeResources": { "friendlyNames": [ { "@type": "asset", "value": { "assetId": ' \
          '"Alexa.Value.Open" } } ] } }, { "value": "Position.Down", "modeResources": { "friendlyNames": [ { "@type": ' \
          '"asset", "value": { "assetId": "Alexa.Value.Close" } } ] } } ] }, "semantics": { "actionMappings": [ { ' \
          '"@type": "ActionsToDirective", "actions": ["Alexa.Actions.Close", "Alexa.Actions.Lower"], "directive": { ' \
          '"name": "SetMode", "payload": { "mode": "Position.Down" } } }, { "@type": "ActionsToDirective", ' \
          '"actions": ["Alexa.Actions.Open", "Alexa.Actions.Raise"], "directive": { "name": "SetMode", "payload": { ' \
          '"mode": "Position.Up" } } } ], "stateMappings": [ { "@type": "StatesToValue", "states": [' \
          '"Alexa.States.Closed"], "value": "Position.Down" }, { "@type": "StatesToValue", "states": [' \
          '"Alexa.States.Open"], "value": "Position.Up" } ] } }, { "type": "AlexaInterface", "interface": "Alexa", ' \
          '"version": "3" } ] } ] } } } '
data = json.loads(jsontxt)

print(jsontxt)
