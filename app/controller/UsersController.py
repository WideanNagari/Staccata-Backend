from app.model.users import Users

from app import app, db
from app.model import response
from flask import request
from flask_jwt_extended import *
from datetime import datetime, timedelta

def formatDataUser(data):
    data = {
        'id': data.id,
        'username': data.username,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'email': data.email,
        'password': data.password,
        'file_converted_piano': data.file_converted_piano,
        'file_converted_guitar': data.file_converted_guitar,
        'report_sent': data.report_sent,
        'level': data.level,
        'created_at': data.created_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'updated_at': data.updated_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'deleted_at': data.deleted_at.strftime('%A, %d %B %Y %H:%M:%S') if data.deleted_at else data.deleted_at
    }
    return data

def formatArray(data):
    arr = []
    for i in data:
        arr.append(formatDataUser(i))
    return arr

@app.route('/api/users', methods=['GET'])
def getAllUser():
    try:
        user = Users.query.all()
        data = formatArray(user)
        return response.success(data, "success")
    except Exception as e:
        return response.serverError({}, str(e))

@app.route('/api/users/<id>', methods=['GET'])
def getOneUser(id):
    try: 
        user = Users.query.filter_by(id=id).first()

        if not user:
            return response.notFound({}, "tidak ada data user")
        
        data = formatDataUser(user)
        return response.success(data, "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/users/summary', methods=['GET'])
def getUserSummary():
    try: 
        users = len(Users.query.all())
        
        return response.success({
            "user_count": users
        }, "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/users', methods=['POST'])
def createUser():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        level = request.json["level"]

        user_check = Users.query.filter_by(username=username).first()
        if(user_check):
            return response.badRequest({}, "Username already registered!")
        
        user_check = Users.query.filter_by(email=email).first()
        if(user_check):
            return response.badRequest({}, "Email already registered!")

        user = Users(username=username, email=email, password=password, level=level)
        user.setPassword(password)
        db.session.add(user)
        db.session.commit()

        return response.success(formatDataUser(user), "Sukses menambah data user")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/users/<id>', methods=['PUT'])
def updateUser(id):
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]

        user = Users.query.filter_by(id=id).filter(Users.deleted_at==None).first()
        
        if not user:
            return response.notFound({}, "tidak ada data user")

        user_check = Users.query.filter_by(username=username).first()
        if(user_check):
            return response.badRequest({}, "Username already registered!")
        
        user_check = Users.query.filter_by(email=email).first()
        if(user_check):
            return response.badRequest({}, "Email already registered!")
        
        user.username = username
        user.email = email
        # user.password = password
        user.setPassword(password)
        user.updated_at = datetime.now()

        db.session.commit()

        return response.success(formatDataUser(user), "Sukses update data user")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/users/advanced/<id>', methods=['PUT'])
def updateUser2(id):
    try:
        firstName = request.json["first_name"]
        lastName = request.json["last_name"]

        user = Users.query.filter_by(id=id).filter(Users.deleted_at==None).first()
        
        if not user:
            return response.notFound({}, "tidak ada data user")

        user.first_name = firstName
        user.last_name = lastName
        user.updated_at = datetime.now()
        
        db.session.commit()

        return response.success(formatDataUser(user), "Sukses update data user")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/users/<id>', methods=['DELETE'])
def deleteUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        
        if not user:
            return response.notFound({}, "tidak ada data user")

        # db.session.delete(user)
        if(user.deleted_at==None):
            user.deleted_at = datetime.now()
        else:
            user.deleted_at = None
        db.session.commit()

        return response.success(formatDataUser(user), "Sukses hapus data user")
    
    except Exception as e:
        return response.serverError({}, str(e))

            