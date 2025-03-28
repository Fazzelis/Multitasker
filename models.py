from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    email = Column(String, unique=True)
    name = Column(String, unique=True)
    avatar = Column(String, unique=True)
    hashed_password = Column(String)
    reset_code = relationship("ResetCode", back_populates="user", uselist=False)


class ResetCode(Base):
    __tablename__ = "reset_code"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4())
    hashed_code = Column(String, unique=True)
    expiration_time = Column(Time)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="reset_code")
