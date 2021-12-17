import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, JSON
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from . import db


class GenderEnum(enum.Enum):
    male = 1
    female = 2
    other = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())


class User(BaseModel):
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_teacher = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)


class Policy(BaseModel):
    key = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    value = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)

    def __str__(self):
        return self.name


subject_student = db.Table('subject_student',
                           Column('subject_id', Integer,
                                  ForeignKey('subject.id')),
                           Column('student_id', Integer,
                                  ForeignKey('student.id')),
                           Column('test15', JSON),
                           Column('test45', JSON),
                           Column('final_test', Integer))


class student(BaseModel):
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    subjects = relationship(
        'Subject', secondary=subject_student, backref='students', lazy=True)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship('Level', backref='subjects', lazy=True)

    def __str__(self):
        return self.name


class level(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)

    def __str__(self):
        return self.name


classroom_student = db.Table('classroom_student',
                             Column('classroom_id', Integer,
                                    ForeignKey('classroom.id')),
                             Column('student_id', Integer, ForeignKey('student.id')))


class classroom(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"))
    level = relationship("level", backref="classrooms", lazy=True)
    students = relationship(
        "Student", secondary=classroom_student, backref="classrooms", lazy=True)

    def __str__(self):
        return self.name


def migrate():
    db.create_all()


if __name__ == '__main__':
    migrate()
