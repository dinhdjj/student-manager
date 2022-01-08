import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, JSON
from datetime import datetime
from flask_login import UserMixin

from sqlalchemy.orm import backref, relationship
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


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_teacher = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    def __str__(self) -> str:
        return self.name


class Policy(BaseModel):
    key = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    value = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)

    def __str__(self):
        return self.name


# subject_student = db.Table('subject_student',
#                            Column('subject_id', Integer,
#                                   ForeignKey('subject.id'), nullable=False),
#                            Column('student_id', Integer,
#                                   ForeignKey('student.id'), nullable=False),
#                            Column('test15', JSON),
#                            Column('test45', JSON),
#                            Column('final_test', Integer), extend_existing=True)


class SubjectStudent(BaseModel):
    __name__ = 'subject_student'
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    s1_test15 = Column(JSON)
    s1_test45 = Column(JSON)
    s1_final_test = Column(Integer)
    s2_test15 = Column(JSON)
    s2_test45 = Column(JSON)
    s2_final_test = Column(Integer)

    subject = relationship('Subject', backref='subject_students')
    student = relationship('Student', backref='subject_students')

    def __str__(self):
        return self.subject.name + ' - ' + self.student.name


class Student(BaseModel):
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    subjects = relationship(
        'Subject', secondary='subject_student', backref='students', lazy=True)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    classroom_id = Column(Integer, ForeignKey('classroom.id'), nullable=False)
    classroom = relationship('Classroom', backref='subjects', lazy=True)
    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    teacher = relationship('User', backref='subjects', lazy=True)

    def __str__(self):
        return self.name


class Level(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    subject_names = Column(JSON, nullable=False)

    def __str__(self):
        return self.name


# classroom_student = db.Table('classroom_student',
#                              Column('classroom_id', Integer,
#                                     ForeignKey('classroom.id'), nullable=False),
#                              Column('student_id', Integer, ForeignKey('student.id'), nullable=False))

class ClassroomStudent(BaseModel):
    __name__ = 'classroom_student'
    classroom_id = Column(Integer, ForeignKey('classroom.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)

    classroom = relationship('Classroom', backref='classroom_students')
    student = relationship('Student', backref='classroom_students')

    def __str__(self):
        return self.classroom.name + ' - ' + self.student.name


class Classroom(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    level = relationship("Level", backref="classrooms", lazy=True)
    students = relationship(
        "Student", secondary='classroom_student', backref="classrooms", lazy=True)

    def __str__(self):
        return self.name


def migrate():
    db.create_all()


if __name__ == '__main__':
    migrate()
