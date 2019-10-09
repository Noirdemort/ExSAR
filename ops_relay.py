from flask import Flask, request
from ops_engine import *
import os
import json
import requests

app = Flask(__name__)


def generate_response(rules, data):
    rs = DecisionTree(data)
    exfil = {}
    try:
        rx = rs.execute_tree(rules)
        exfil['message'] = str(rx)
        status_code = 200
    except Exception as e:
        exfil['message'] = str(e)
        status_code = 400
    
    response = app.response_class(response=json.dumps(exfil), status=status_code, mimetype='application/json')
    return response


@app.route("/")
def hello_world():
    return "Hello friend! This is ExSAR (Execution Sat And Relay) and you have execute authority under Captain Price."


@app.route("/payload/dangerClose", methods=["POST"])
def execute_auth():
    '''
    API endpoint: /payload/dangerClose
    Method = "POST"
    JSON Query: {"rule": {}, "validationSet": {}}

    JSON Response: success 200 OK, 
                    json body: {"message":"<True | False>"} or
                    
                    failed 40x BAD Request,
                    json body: {"message": Reason of Failure}
                    
    '''
    contact = request.json
    if 'validationSet' not in contact or 'rule' not in contact:
        exfil = json.dumps({"message": "Rule and Validation Data are required!!"})
        response = app.response_class(response=exfil, status=403, mimetype='application/json')
        return response
    
    data = contact['validationSet']
    rules = contact['rule']
    return generate_response(rules, data)
    


@app.route('/remote/dangerClose', methods=['POST'])
def exec_remote_auth():
    '''
    API endpoint: /remote/dangerClose
    Method = "POST"
    JSON Query: {"ruleLink": "string", "validationSet": {}}

    JSON Response: success 200 OK, 
                    json body: {"message":"<True | False>"} or
                    
                    failed 40x ,
                    json body: {"message": Reason of Failure}
                    
    '''
    contact = request.json
    if 'validationSet' not in contact or 'ruleLink' not in contact:
        exfil = json.dumps({"message": "Rule and Validation Data are required!!"})
        response = app.response_class(response=exfil, status=403, mimetype='application/json')
        return response
    
    data = contact['validationSet']
    r = requests.get(contact['ruleLink'])
    if r.status_code == 200:
        rules = json.loads(r.text)
        return generate_response(rules, data)
    else:
        exfil = json.dumps({"message": "Can't fetch rules!!"})
        response = app.response_class(response=exfil, status=402, mimetype='application/json')
        return response
    

 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)