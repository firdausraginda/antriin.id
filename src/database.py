from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random, string, enum

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
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    queues = db.relationship('Queue', backref='admin', lazy=True)

    def __repr__(self):
        return '<Admin %r>' % self.email

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.name

class QueueUserStatus(enum.Enum):
    in_queue = "in_queue"
    done = "done"

class QueueUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(QueueUserStatus), nullable=False, default="in_queque")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return '<QueueUser %r>' % self.queue_id

class QueueStatus(enum.Enum):
    active = "active"
    hold = "hold"
    off = "off"

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(QueueStatus), nullable=False, default="off")
    short_url = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def generate_short_url(self):
        random_string = ''.join(random.choices(string.ascii_letters, k=5))
        query_result = self.query.filter_by(short_url=random_string).first()
        
        if query_result:
            self.generate_short_url()
        else:
            return random_string
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_url()
    
    def __repr__(self):
        return '<Queue %r>' % self.name