import requests
from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
def index():
    header = {
        "DD-API-KEY": "985c561cc770a786c91893eba6dbacfa"
    }
    response = requests.get("https://api.datadoghq.com/api/v1/validate",headers=header)

    if response.ok:
        return response.text
    else:
        return "Error Occured while validation"


if __name__ == "__main__":
    app.run(port=9999,debug=True)
