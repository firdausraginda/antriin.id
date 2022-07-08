from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.String, nullable=True)

    admins = db.relationship('Admin', backref='org', lazy=True)

    def __repr__(self):
        return '<Organization %r>' % self.name

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.email