from app import app
from app.model import response
from flask import request, make_response
import json

@app.route('/api/set_cookie', methods=['POST'])
def set_cookie():
    try:
        name = request.json["name"]
        value = request.json["value"]
        # print(name)
        # print(json.dumps(value))
        resp = make_response('Cookie has been set', 200)
        resp.set_cookie(name, json.dumps(value))
        return resp

    except Exception as e:
        return response.badRequest({}, str(e))

@app.route('/api/get_cookie/<name>', methods=['GET'])
def get_cookie(name):
    try:
        cookie_value = request.cookies.get(name)
        return response.success(json.loads(cookie_value), "success")
    except Exception as e:
        return response.badRequest({}, str(e))