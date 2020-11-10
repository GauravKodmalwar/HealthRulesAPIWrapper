import requests
from json2html import *
import json
from flask import Flask, url_for, redirect, request, render_template, jsonify
app = Flask(__name__)
from os.path import dirname, join
from flask_cors import CORS, cross_origin
#------------------------------GET API---------------------------------------

@app.route('/')
@cross_origin()
def index():
    return render_template('Dynatrace.html')


@app.route("/GetApllicationList/<AppdynamicsHost>")
@cross_origin()
def GetApllicationList(AppdynamicsHost):

    Url = "https://" + AppdynamicsHost + ".saas.appdynamics.com/controller/rest/applications?output=JSON"
    # data =GetValueFromJson()
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.get(Url, headers=header)
    Result = response.text
    responseobj = app.response_class(
        response = Result,
        mimetype='application/json'
    )
    if response.ok:
        return responseobj
    else:
        return "Error occured while getting Application list"

@app.route("/GetHealthRules/<AppdynamicsHost>/<ApplicationId>")
@cross_origin()
def GetHealthRules(AppdynamicsHost,ApplicationId):

    Url = "https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/health-rules?output=JSON"
    # data =GetValueFromJson()
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.get(Url, headers=header)
    result = response.text
    responseobj = app.response_class(
        response=result,
        mimetype='application/json'
    )
    if response.ok:
        return responseobj
    else:
        return "Error occured while getting Health Rules"

@app.route("/GetEmailDigest/<AppdynamicsHost>/<ApplicationId>")
@cross_origin()
def GetEmailDigest(AppdynamicsHost,ApplicationId):

    Url = "https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/email-digests"
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.get(Url, headers=header)
    result = response.text
    responseobj = app.response_class(
        response = result,
        mimetype='application/json'
    )
    if response.ok:
        return responseobj
    else:
        return "Error occured while getting Email Digest"


@app.route("/GetActions/<AppdynamicsHost>/<ApplicationId>")
@cross_origin()
def GetActions(AppdynamicsHost,ApplicationId):

    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/actions"
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.get(Url, headers=header)
    result = response.text
    responseobj = app.response_class(
        response = result,
        mimetype='application/json'
    )
    if response.ok:
        return responseobj
    else:
        return "Error occured while getting Actions"


@app.route("/GetPolicy/<AppdynamicsHost>/<ApplicationId>")
@cross_origin()
def GetPolicy(AppdynamicsHost,ApplicationId):

    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/policies"
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.get(Url, headers=header)
    result = response.text
    responseobj = app.response_class(
        response=result,
        mimetype='application/json'
    )
    if response.ok:
        return responseobj
    else:
        return "Error occured while getting Policies"


#------------------------------GET API END---------------------------------------

#------------------------------POST API---------------------------------------
@app.route("/CreateHealthRule/<AppdynamicsHost>/<ApplicationId>", methods=['POST'])
@cross_origin()
def CreateHealthRule(AppdynamicsHost,ApplicationId):
    filename = request.data
    filename = json.loads(filename)
    jsonvalue = GetValueFromJson("HealthRule/"+filename["FileName"] + ".JSON")
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    jsonvalue = json.dumps(jsonvalue)
    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/health-rules"
    response = requests.post(Url,headers=header,data=jsonvalue)

    if response.ok:
        return "Sucessfully created."
    else:
        return "Error Occured while creating health rule"

@app.route("/CreateEmailDigest/<AppdynamicsHost>/<ApplicationId>", methods=['POST'])
@cross_origin()
def CreateEmailDigest(AppdynamicsHost,ApplicationId):
    jsonvalue = request.data
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    # jsonvalue = json.loads(jsonvalue)
    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/email-digests"
    response = requests.post(Url,headers=header,data=jsonvalue)

    if response.ok:
        return "Sucessfully created."
    else:
        return "Error Occured while creating Email digest"

@app.route("/CreateAction/<AppdynamicsHost>/<ApplicationId>", methods=['POST'])
@cross_origin()
def CreateAction(AppdynamicsHost,ApplicationId):
    jsonvalue = request.data
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    # jsonvalue = json.loads(jsonvalue)
    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/actions"
    response = requests.post(Url,headers=header,data=jsonvalue)

    if response.ok:
        return "Sucessfully created Action."
    else:
        return "Error Occured while creating Action"

@app.route("/CreatePolicy/<AppdynamicsHost>/<ApplicationId>", methods=['POST'])
@cross_origin()
def CreatePolicy(AppdynamicsHost,ApplicationId):
    jsonvalue = request.data
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    # jsonvalue = json.loads(jsonvalue)
    Url ="https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/policies"
    response = requests.post(Url,headers=header,data=jsonvalue)

    if response.ok:
        return "Sucessfully created Action."
    else:
        return "Error Occured while creating Action"

#------------------------------POST API END---------------------------------------

#-----------------------------Delete API -----------------------------------------
@app.route("/DeleteEmailDigestById/<AppdynamicsHost>/<ApplicationId>/<EmailDigestId>")
@cross_origin()
def DeleteEmailDigestById(AppdynamicsHost,ApplicationId,EmailDigestId):

    Url = "https://"+ AppdynamicsHost +".saas.appdynamics.com/controller/alerting/rest/v1/applications/"+ApplicationId+"/email-digests/"+EmailDigestId
    headervalue = request.headers['Authorization']
    header = {
        "Authorization": headervalue,
        "Content-Type": "application/json"
    }
    response = requests.delete(Url, headers=header)
    result = response.text
    if response.ok:
        return "Email digest deleted sucessfully"
    else:
        return "Error occured while getting Email Digest"


#-----------------------------Delete End API -----------------------------------------

#----------------------Function------------------------------------------------

def GetValueFromJson(filename):
    here = dirname(__file__)
    output = join(here, filename)
    with open(output) as f:
        data = json.load(f)
    return data
#------------------------------------ Function End------------------------------

if __name__ == "__main__":
    app.run(port=5000, debug=True)
