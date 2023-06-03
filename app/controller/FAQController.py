from app.model.faq import FAQ

from app import app, db
from app.model import response
from flask import request
from datetime import datetime

def formatDataFAQ(data):
    data = {
        'id': data.id,
        'question': data.question,
        'answer': data.answer,
        'created_at': data.created_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'updated_at': data.updated_at.strftime('%A, %d %B %Y %H:%M:%S'),
        'deleted_at': data.deleted_at.strftime('%A, %d %B %Y %H:%M:%S') if data.deleted_at else data.deleted_at
    }
    return data

def formatArrayFAQ(data):
    arr = []
    for i in data:
        arr.append(formatDataFAQ(i))
    return arr

@app.route('/api/faq', methods=['GET'])
def getAllFAQ():
    try:
        faq = FAQ.query.all()
        data = formatArrayFAQ(faq)
        return response.success(data, "success")
    except Exception as e:
        return response.serverError({}, str(e))

@app.route('/api/faq/<id>', methods=['GET'])
def getOneFAQ(id):
    try: 
        faq = FAQ.query.filter_by(id=id).first()

        if not faq:
            return response.notFound({}, "tidak ada data FAQ")
        
        return response.success(formatDataFAQ(faq), "success")

    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/faq', methods=['POST'])
def createFAQ():
    try:
        question = request.json["question"]
        answer = request.json["answer"]

        faq = FAQ(question=question, answer=answer)
        db.session.add(faq)
        db.session.commit()

        return response.success(formatDataFAQ(faq), "Sukses menambah data FAQ")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/faq/<id>', methods=['PUT'])
def updateFAQ(id):
    try:
        question = request.json["question"]
        answer = request.json["answer"]

        faq = FAQ.query.filter_by(id=id).filter(FAQ.deleted_at==None).first()
        
        if not faq:
            return response.notFound({}, "tidak ada data FAQ")

        faq.question = question
        faq.answer = answer
        faq.updated_at = datetime.now()
        
        db.session.commit()

        return response.success(formatDataFAQ(faq), "Sukses update data FAQ")
    
    except Exception as e:
        return response.serverError({}, str(e))
    
@app.route('/api/faq/<id>', methods=['DELETE'])
def deleteFAQ(id):
    try:
        faq = FAQ.query.filter_by(id=id).first()
        
        if not faq:
            return response.notFound({}, "tidak ada data FAQ")
        
        if(faq.deleted_at==None):
            faq.deleted_at = datetime.now()
        else:
            faq.deleted_at = None
            
        # db.session.delete(faq)
        db.session.commit()
        
        return response.success(formatDataFAQ(faq), "Sukses hapus data FAQ")
    
    except Exception as e:
        return response.serverError({}, str(e))

            