from app import db
from datetime import datetime
from app.model.users import Users

class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reporter = db.Column(db.Integer, db.ForeignKey(Users.id))
    reporter_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Report {}>'.format(self.reporter)