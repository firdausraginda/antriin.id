from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime
import random, string

db = SQLAlchemy()


class SuperAdmin(db.Model):
    __tablename__ = "super_admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organization = db.relationship(
        "Organization", backref="super_admin", lazy=True, uselist=False
    )

    def __repr__(self):
        return "<Super Admin %r>" % self.email


class Organization(db.Model):
    __tablename__ = "organization"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    super_admin_id = db.Column(
        db.Integer, db.ForeignKey("super_admin.id"), nullable=False, unique=True
    )

    admins = db.relationship("Admin", backref="organization", lazy=True)

    def __repr__(self):
        return "<Organization %r>" % self.name


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )

    queues = db.relationship("Queue", backref="admin", lazy=True)

    def __repr__(self):
        return "<Admin %r>" % self.email


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    queues_users = db.relationship("QueueUser", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.name


class QueueUser(db.Model):
    __tablename__ = "queue_user"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        Enum("in_queue", "done", validate_strings=True),
        nullable=False,
        default="in_queue",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    queue_id = db.Column(db.Integer, db.ForeignKey("queue.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<QueueUser %r>" % self.queue_id


class Queue(db.Model):
    __tablename__ = "queue"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    status = db.Column(
        Enum("active", "hold", "off", validate_strings=True),
        nullable=False,
        default="off",
    )
    short_url = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)

    queues_users = db.relationship("QueueUser", backref="queue", lazy=True)

    def generate_short_url(self):
        random_string = "".join(random.choices(string.ascii_letters, k=5))
        query_result = self.query.filter_by(short_url=random_string).first()

        if query_result:
            self.generate_short_url()
        else:
            return random_string

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_url()

    def __repr__(self):
        return "<Queue %r>" % self.name
