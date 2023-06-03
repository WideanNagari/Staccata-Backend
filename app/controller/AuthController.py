from app.model.users import Users

from app import app, db
from app.model import response
from flask import request
from flask_jwt_extended import *
from datetime import datetime, timedelta

def formatJWT(data):
    data = {
        'id': data.id,
        'username': data.username,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'level': data.level,
        'file_converted_piano': data.file_converted_piano,
        'file_converted_guitar': data.file_converted_guitar,
        'report_sent': data.report_sent
    }
    return data

@app.route('/api/login', methods=['POST'])
def login():
    try:
        username = request.json["username"]
        password = request.json["password"]

        user = Users.query.filter_by(username=username).first()
        
        if not user:
            return response.badRequest({}, "No user data")
        
        if user.deleted_at!=None:
            return response.badRequest({}, "You're under banned!")
        
        if not user.checkPassword(password):
            return response.badRequest({}, "The password is wrong!")
        
        data = formatJWT(user)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data": data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, "Login success")
    except Exception as e:
        return response.badRequest({}, e)
