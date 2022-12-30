from sqlmodel import Field, Relationship, SQLModel, Enum, Column
from typing import List
from datetime import datetime
import enum, random, string

class SuperAdmin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow)

    organization_1: "Organization" = Relationship(back_populates="super_admin")

class Organization(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow)
    description: str = Field(nullable=True)
    super_admin_id: int = Field(foreign_key="super_admin.id", nullable=False)

    super_admin: SuperAdmin = Relationship(back_populates="organization_1")
    admins: List["Admin"] = Relationship(back_populates="organization_2")

class Admin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow)
    organization_id: int = Field(foreign_key="organization_2.id", nullable=False)

    organization_2: Organization = Relationship(back_populates="admins")
    queues: List["Queue"] = Relationship(back_populates="admin")

class QueueStatus(str, enum.Enum):
    active = "active"
    hold = "hold"
    off = "off"

class Queue(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(onupdate=datetime.utcnow)
    description: str = Field(nullable=True)
    status: QueueStatus = Field(sa_column=Column(Enum(QueueStatus)), nullable=False, default="off")
    short_url: str = Field(nullable=False)
    admin_id: int = Field(foreign_key="admin.id", nullable=False)

    admin: Admin = Relationship(back_populates="queues")
    queueusers_1: List["QueueUser"] = Relationship(back_populates="queue")

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

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.utcnow)

    queueusers_2: List["QueueUser"] = Relationship(back_populates="user")

class QueueUserStatus(str, enum.Enum):
    in_queue = "in_queue"
    done = "done"

class QueueUser(SQLModel, table=True):
    id: int = Field(primary_key=True)
    status: QueueUserStatus = Field(sa_column=Column(Enum(QueueUserStatus)), nullable=False, default="in_queue")
    created_at: datetime = Field(default=datetime.utcnow)
    updated_at: datetime = Field(onupdate=datetime.utcnow)
    queue_id: int = Field(foreign_key="queue.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)

    queue: Queue = Relationship(back_populates="queueusers_1")
    user: User = Relationship(back_populates="queueusers_2")


