from sqlmodel import Field, Relationship, SQLModel, Enum, Column, DateTime
from typing import List, Optional
from datetime import datetime
import enum
from sqlalchemy.sql import func


class Organization(SQLModel, table=True):
    __tablename__ = "organization"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
    description: str = Field(nullable=True)
    admin_id: int = Field(foreign_key="admin.id", nullable=False, unique=True)

    admin: "Admin" = Relationship(back_populates="organization")


class Admin(SQLModel, table=True):
    __tablename__ = "admin"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )

    organization: Organization = Relationship(back_populates="admin")
    queues: List["Queue"] = Relationship(back_populates="admin")


class QueueStatus(str, enum.Enum):
    active = "active"
    hold = "hold"
    off = "off"


class Queue(SQLModel, table=True):
    __tablename__ = "queue"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False, unique=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
    description: str = Field(nullable=True)
    status: QueueStatus = Field(
        sa_column=Column(Enum(QueueStatus)), default=QueueStatus.off
    )
    short_url: str = Field(nullable=False, unique=True)
    current_queue_number: int = Field(nullable=False, default=0)
    total_queue_number: int = Field(nullable=False, default=0)
    admin_id: int = Field(foreign_key="admin.id", nullable=False)

    admin: Admin = Relationship(back_populates="queues")
    queueusers: List["QueueUser"] = Relationship(back_populates="queue")


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )

    queueusers: List["QueueUser"] = Relationship(back_populates="user")


class QueueUserStatus(str, enum.Enum):
    in_queue = "in_queue"
    done = "done"


class QueueUser(SQLModel, table=True):
    __tablename__ = "queue_user"
    id: Optional[int] = Field(primary_key=True)
    status: QueueUserStatus = Field(
        sa_column=Column(Enum(QueueUserStatus)), default=QueueUserStatus.in_queue
    )
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
    queue_number: int
    queue_id: int = Field(foreign_key="queue.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)

    queue: Queue = Relationship(back_populates="queueusers")
    user: User = Relationship(back_populates="queueusers")
