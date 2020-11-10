import requests
from json2html import *
import json
from flask import Flask, url_for, redirect, request, render_template
app = Flask(__name__)
from os.path import dirname, join
from flask_cors import CORS, cross_origin

@app.route('/')
@cross_origin()
def index():
    return render_template('Dynatrace.html')

@app.route("/ValidateDynaTrace")
@cross_origin()
def ValidateDynaTrace():
    Json_readData = GetValueFromJson()
    Url = "https://" + Json_readData['dynatraceHost'] + ".live.dynatrace.com/api/v1/config/clusterversion"
    header = {
        "Authorization": "Api-Token " + Json_readData['dynatracetoken']
    }
    response = requests.get(Url,headers=header)

    if response.ok:
        return response.text
    else:
        return "Error Occured while validation"

@app.route("/GetAlertProfile/<dynatracetoken>/<dynatraceHost>")
@cross_origin()
def GetAlertProfile(dynatracetoken,dynatraceHost):
    Json_readData = GetValueFromJson()
    # Url = "https://" + Json_readData['dynatraceHost'] + ".live.dynatrace.com/api/config/v1/alertingProfiles"
    Url = "https://" + dynatraceHost + ".live.dynatrace.com/api/config/v1/alertingProfiles"
    header = {
        # "Authorization": "Api-Token " + Json_readData['dynatracetoken'],
        "Authorization": "Api-Token " + dynatracetoken,
        "Content-Type":"application/json"
    }
    response = requests.get(Url,headers=header)
    result = response.text.replace("values","")[:-1][4:]
    if response.ok:
        # return   json2html.convert(json = result)
        return result
    else:
        return "Error Occured while Fetching Alert Profiles"

@app.route("/GetNotificaltionConfiguration/<dynatracetoken>/<dynatraceHost>")
@cross_origin()
def GetNotificaltionConfiguration(dynatracetoken,dynatraceHost):
    Json_readData = GetValueFromJson()
    # Url = "https://" + Json_readData['dynatraceHost']  + ".live.dynatrace.com/api/config/v1/notifications"
    Url = "https://" + dynatraceHost + ".live.dynatrace.com/api/config/v1/notifications"
    header = {
        "Authorization": "Api-Token " + dynatracetoken
    }
    response = requests.get(Url ,headers=header)
    result = response.text.replace("values", "")[:-1][4:]
    if response.ok:
        # return json2html.convert(json = result)
        return result
    else:
        return "Error Occured while fetching configuration"

@app.route("/GetAnamolyHost")
@cross_origin()
def GetAnamolyHost():
    Json_readData = GetValueFromJson()
    Url = "https://" + Json_readData['dynatraceHost'] + ".live.dynatrace.com/api/config/v1/anomalyDetection/hosts"
    header = {
        "Authorization": "Api-Token " + Json_readData['dynatracetoken']
    }
    response = requests.get(Url,headers=header)

    if response.ok:
        return response.text
    else:
        return "Error Occured while fetching Anamoly Host"

@app.route("/GetAnamolyApplication")
@cross_origin()
def GetAnamolyApplication():
    Json_readData = GetValueFromJson()
    Url="https://"+Json_readData['dynatraceHost']+".live.dynatrace.com/api/config/v1/anomalyDetection/applications"
    header = {
        "Authorization": "Api-Token "+ Json_readData['dynatracetoken']
    }
    response = requests.get(Url,headers=header)

    if response.ok:
        return response.text
    else:
        return "Error Occured while fetching Anamoly Application"

# @app.route("/GetAnamolyServices/<HostName>")
@app.route("/GetAnamolyServices")
@cross_origin()
def GetAnamolyServices():
        Json_readData = GetValueFromJson()
        Url="https://"+Json_readData['dynatraceHost']+".live.dynatrace.com/api/config/v1/anomalyDetection/services"
        header = {
            "Authorization": "Api-Token "+ Json_readData['dynatracetoken']
        }
        response = requests.get(Url,
                                headers=header)

        if response.ok:
            return response.text
        else:
            return "Error Occured while fetching Anamoly Services"

#----------------------Function------------------------------------------------

def GetValueFromJson():
    here = dirname(__file__)
    output = join(here, 'Configuration.json')
    with open(output) as f:
        data = json.load(f)
    return data

#----------------------Post API-------------------------------------------------

@app.route("/CreateAlertProfile", methods=['POST'])
@cross_origin()
def CreateAlertProfile():
    jsonvalue = request.form
    header = {
       # "Authorization": "Api-Token ifQ4bfP-R-KLsOgLn_NkL",
        "Authorization": "Api-Token " +jsonvalue['APIToken'],
        "Content-Type": "application/json"
    }
    Rules =request.form.getlist('Rule')
    RuleData =''
    for i in Rules:
        RuleData = RuleData +  '{ "severityLevel" : "' + i +'", "tagFilter" : { "includeMode" : "INCLUDE_ALL" }, "delayInMinutes" : "60"}, '

    RuleData = "[ "+RuleData.rstrip()[:-1] +" ]"

    data = '{ "displayName" : "'+ jsonvalue['ProfileName'] +'","rules":'+ RuleData +' }'
    # Jsondata = json.dumps(data)
    Url ="https://"+jsonvalue['HostName']+".live.dynatrace.com/api/config/v1/alertingProfiles"

    response = requests.post(Url,headers=header,data=data)

    if response.ok:
        return "Sucessfully created profile"
    else:
        return "Error Occured while creating alert profile"


@app.route("/CreateAlertProfilePostman/<Hostname>", methods=['POST'])
@cross_origin()
def CreateAlertProfilePostman(Hostname):
    jsonvalue = request.data
    headervalue = request.headers['Authorization']
    header = {
       # "Authorization": "Api-Token ifQ4bfP-R-KLsOgLn_NkL",
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    json_readData = json.loads(jsonvalue)
    Rules =json_readData['rules']
    RuleData =''
    for i in Rules:
        RuleData = RuleData +  '{ "severityLevel" : "' + i['severityLevel'] +'", "tagFilter" : { "includeMode" : "INCLUDE_ALL" }, "delayInMinutes" : "60"}, '

    RuleData = "[ "+RuleData.rstrip()[:-1] +" ]"

    data = '{ "displayName" : "'+ json_readData['displayName'] +'","rules":'+ RuleData +' }'
    Url = "https://" + Hostname + ".live.dynatrace.com/api/config/v1/alertingProfiles"

    response = requests.post(Url,headers=header,data=data)

    if response.ok:
        return "Sucessfully created profile"
    else:
        return "Error Occured while creating alert profile"

@app.route("/CreateNotificationConfig", methods=['POST'])
@cross_origin()
def CreateNotificationConfig():
    jsonvalue = request.form
    header = {
        # "Authorization": "Api-Token ifQ4bfP-R-KLsOgLn_NkL",
        "Authorization": "Api-Token " + jsonvalue['APIToken'],
        "Content-Type": "application/json"
    }
     # jsonvalue = request.jsoneggg

    UserInput = jsonvalue['Email']
    EmailIds = UserInput.split(",")

    data = {'type': 'EMAIL', 'name': jsonvalue['Body'], 'alertingProfile': jsonvalue['ProfileId'],
            'active': True, 'subject': 'Dynatrace Notification', 'body': jsonvalue['Body'],
            'receivers': EmailIds,
            'ccReceivers': EmailIds,
            'shouldSendForResolvedProblems': True}
    Jsondata =json.dumps(data)
    response = requests.post("https://hqq84840.live.dynatrace.com/api/config/v1/notifications",headers=header,data=Jsondata)

    if response.ok:
        return "Sucessfully created."
    else:
        return "Error Occured while setting notification configuration"

@app.route("/CreateNotificationConfigPostman/<Hostname>", methods=['POST'])
@cross_origin()
def CreateNotificationConfigPostman(Hostname):
    jsonvalue = request.data
    headervalue = request.headers['Authorization']
    header = {
        # "Authorization": "Api-Token ifQ4bfP-R-KLsOgLn_NkL",
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    jsonvalue = json.loads(jsonvalue)

    UserInput = jsonvalue['receivers']
    # EmailIds = UserInput.split(",")

    data = {'type': 'EMAIL', 'name': jsonvalue['title'], 'alertingProfile': jsonvalue['alertingProfile'],
            'active': True, 'subject': 'State: {State} Process: {PID} Severity: {ProblemSeverity} Reason: {ProblemTitle}  URL: {ProblemURL} Entities: {ImpactedEntity}',
            'body': 'State: {State} Process: {PID} Severity: {ProblemSeverity} Reason: {ProblemTitle}  URL: {ProblemURL} Entities: {ImpactedEntity}',
            'receivers': UserInput,
            'ccReceivers': UserInput,
            'shouldSendForResolvedProblems': True}
    Jsondata =json.dumps(data)
    url="https://"+Hostname+".live.dynatrace.com/api/config/v1/notifications"
    response = requests.post(url,headers=header,data=Jsondata)

    if response.ok:
        return "Sucessfully created."
    else:
        return "Error Occured while setting notification configuration"

#-----------------------------------Delete API---------------------------------

@app.route("/DeleteNotificaltionConfigurationById/<dynatracetoken>/<dynatraceHost>/<Id>",methods=["DELETE"])
@cross_origin()
def DeleteNotificaltionConfigurationById(dynatracetoken,dynatraceHost,Id):
    # Json_readData = GetValueFromJson()
    # Url = "https://" + Json_readData['dynatraceHost']  + ".live.dynatrace.com/api/config/v1/notifications/"+Id
    Url = "https://" + dynatraceHost + ".live.dynatrace.com/api/config/v1/notifications/" + Id
    header = {
        "Authorization": "Api-Token " + dynatracetoken
    }
    response = requests.delete(Url ,headers=header)

    if response.ok:
        return "Record deleted sucessfully"
    else:
        return "Error Occured while fetching configuration"

# ---------------------------------------- Main method ---------------------------------

if __name__ == "__main__":
    app.run(port=5555,debug=True)

#------------------------------------get api-------------------------------
