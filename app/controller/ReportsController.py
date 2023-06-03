from app.model.reports import Reports
from app.model.users import Users
from app.controller.UsersController import formatDataUser

from app import app, db
from app.model import response
from flask import request
from datetime import datetime
from sqlalchemy import func

def formatDataReport(data, reporter):
    data = {
        'id': data.id,
        'title': data.title,
        'description': data.description,
        'reporter': reporter,
        'reporter_name': data.reporter_name,
        'created_at': data.created_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'updated_at': data.updated_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'deleted_at': data.deleted_at.strftime('%A, %d %B %Y %H:%M:%S') if data.deleted_at else data.deleted_at
    }
    return data

def formatArrayReport(data):
    arr = []
    for i in data:
        user = Users.query.filter_by(id=i.reporter).first()
        data_user = formatDataUser(user)
        arr.append(formatDataReport(i, data_user))
    return arr

@app.route('/api/reports', methods=['GET'])
def getAllReport():
    try:
        report = Reports.query.all()

        data = formatArrayReport(report)

        return response.success(data, "success")
    except Exception as e:
        return response.serverError({}, str(e))

@app.route('/api/reports/<id>', methods=['GET'])
def getOneReport(id):
    try: 
        report = Reports.query.filter_by(id=id).first()

        if not report:
            return response.notFound({}, "tidak ada data report")
        
        user = Users.query.filter_by(id=report.reporter).first()
        data_user = formatDataUser(user)
        
        return response.success(formatDataReport(report, data_user), "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/reports/summary', methods=['GET'])
def getReportSummary():
    try: 
        reports = len(Reports.query.all())
        
        return response.success({
            "report_count": reports
        }, "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/reports/top', methods=['GET'])
def getTopReport():
    try: 
        reports = db.session.query(Users.username, func.count(Reports.reporter).label("reporter")).join(Users).group_by(Reports.reporter).order_by(func.count(Reports.reporter).desc()).all()
        res = []
        for i in reports:
            res.append({
                'username': str(i.username),
                'report_count': str(i.reporter)
            })
        
        return response.success(res, "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/reports', methods=['POST'])
def createReport():
    try:
        title = request.json["title"]
        description = request.json["description"]
        reporter = request.json["reporter"]
        reporter_name = request.json["reporter_name"]

        if(title=="" or description=="" or reporter==""):
            return response.badRequest({}, "Mohon isi semua data!")

        report = Reports(title=title, description=description, reporter=int(reporter), reporter_name=reporter_name)
        db.session.add(report)
        db.session.commit()

        user = Users.query.filter_by(id=report.reporter).first()
        data_user = formatDataUser(user)

        return response.success(formatDataReport(report, data_user), "Sukses menambah data report")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/reports/<id>', methods=['PUT'])
def updateReport(id):
    try:
        title = request.json["title"]
        description = request.json["description"]
        reporter = request.json["reporter"]

        report = Reports.query.filter_by(id=id).filter(Reports.deleted_at==None).first()
        
        if not report:
            return response.notFound({}, "tidak ada data report")

        report.title = title
        report.description = description
        report.reporter = int(reporter)
        report.updated_at = datetime.now()
        
        db.session.commit()

        user = Users.query.filter_by(id=report.reporter).first()
        data_user = formatDataUser(user)

        return response.success(formatDataReport(report, data_user), "Sukses update data report")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/reports/<id>', methods=['DELETE'])
def deleteReport(id):
    try:
        report = Reports.query.filter_by(id=id).first()
        
        if not report:
            return response.notFound({}, "tidak ada data report")

        if(report.deleted_at==None):
            report.deleted_at = datetime.now()
        else:
            report.deleted_at = None

        # db.session.delete(report)
        db.session.commit()

        user = Users.query.filter_by(id=report.reporter).first()
        data_user = formatDataUser(user)

        return response.success(formatDataReport(report, data_user), "Sukses hapus data report")
    
    except Exception as e:
        return response.serverError({}, str(e))
            