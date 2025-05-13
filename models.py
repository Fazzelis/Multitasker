from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, func, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.database import Base


user_project_association = Table(
    'user_project_association',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True),
    Column('project_id', UUID(as_uuid=True), ForeignKey('project.id'), primary_key=True)
)

category_project_association = Table(
    'category_project_association',
    Base.metadata,
    Column('category_id', UUID(as_uuid=True), ForeignKey('category.id'), primary_key=True),
    Column('project_id', UUID(as_uuid=True), ForeignKey('project.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    is_admin = Column(Boolean, default=False, server_default="false")
    email = Column(String, unique=True)
    name = Column(String, unique=True)
    hashed_password = Column(String)
    avatar_id = Column(UUID)
    reset_code = relationship("ResetCode", back_populates="user", uselist=False)
    categories = relationship("Category", back_populates="user")
    projects = relationship(
        "Project",
        secondary=user_project_association,
        back_populates="users",
        lazy="dynamic"
    )
    tasks = relationship("Task", back_populates="user")
    subtasks = relationship("SubTask", back_populates="user")


class Attachment(Base):
    __tablename__ = "attachment"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    attachment_path = Column(String, unique=True)


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
    projects = relationship(
        "Project",
        secondary=category_project_association,
        back_populates="categories",
        cascade="all, delete",
        lazy="dynamic"
    )


class Project(Base):
    __tablename__ = "project"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    creator = relationship("User", foreign_keys=[creator_id])
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    users = relationship(
        "User",
        secondary=user_project_association,
        back_populates="projects",
        lazy="dynamic"
    )
    categories = relationship(
        "Category",
        secondary=category_project_association,
        back_populates="projects",
        lazy="dynamic"
    )


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
    sub_tasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan", lazy="joined")


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
