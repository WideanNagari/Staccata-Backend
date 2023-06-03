from app import db
from datetime import datetime
from app.model.users import Users

class Performances(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    initial = db.Column(db.String(6), nullable=False)
    target = db.Column(db.String(6), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(Users.id))
    duration = db.Column(db.Integer, nullable=False)
    like_status = db.Column(db.Integer, nullable=True)
    gdrive_link = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(Users.id))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Performances {}>'.format(self.title)