from sqlalchemy import Column, Integer, String, ForeignKey, Time, Boolean, Table, Date, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    email = Column(String, unique=True)
    name = Column(String, unique=True)
    avatar = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)
    reset_code = relationship("ResetCode", back_populates="user", uselist=False)
    categories = relationship("Category", back_populates="user")
    projects = relationship("Project", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    subtasks = relationship("SubTask", back_populates="user")


class ResetCode(Base):
    __tablename__ = "reset_code"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    hashed_code = Column(String, unique=True)
    expiration_time = Column(Time)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="reset_code")


class Category(Base):
    __tablename__ = "category"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="categories")
    projects = relationship("Project", back_populates="category", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True)
    avatar_path = Column(String, unique=True, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id", ondelete="CASCADE"))
    category = relationship("Category", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="projects")


class Task(Base):
    __tablename__ = "task"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True)
    description = Column(String)
    due_date = Column(Date)
    indicator = Column(Integer)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="tasks")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="tasks")
    sub_tasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")


class SubTask(Base):
    __tablename__ = "sub_task"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True)
    description = Column(String)
    due_date = Column(Date)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="subtasks")
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id", ondelete="CASCADE"))
    task = relationship("Task", back_populates="sub_tasks")
