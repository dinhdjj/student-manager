import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, JSON, Float
from datetime import datetime
from flask_login import UserMixin
import hashlib

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
    value = Column(Integer, nullable=False)
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
    s1_final_test = Column(Float)
    s2_test15 = Column(JSON)
    s2_test45 = Column(JSON)
    s2_final_test = Column(Float)

    subject = relationship('Subject', backref='subject_students')
    student = relationship('Student', backref='subject_students')

    def __str__(self):
        return self.subject.name + ' - ' + self.student.name


class Student(BaseModel):
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    subjects = relationship(
        'Subject', secondary='subject_student', backref='students', lazy=True)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = Column(String(50), nullable=False)
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
    year = Column(Integer, nullable=False)
    students = relationship(
        "Student", secondary='classroom_student', backref="classrooms", lazy=True)

    def __str__(self):
        return self.name


def migrate():
    db.create_all()

    db.session.add(Policy(key='min_age', name='tuổi nhập học tối thiểu',
                          value=15, description='Tuổi nhập học tối thiểu'))
    db.session.add(Policy(key='max_age', name='tuổi nhập học tối đa',
                          value=20, description='Tuổi nhập học tối đa'))

    db.session.add(Policy(key='max_amount', name='số lượng học sinh tối đa',
                          value=40, description='Số lượng học sinh tối đa'))

    db.session.add(Policy(key='min_test15', name='số lượng tối thiểu điểm 15 phút',
                          value=1, description='số lượng tối thiểu điểm 15 phút'))
    db.session.add(Policy(key='max_test15', name='số lượng tối đa điểm 15 phút',
                          value=5, description='số lượng tối đa điểm 15 phút'))

    db.session.add(Policy(key='min_test45', name='số lượng tối thiểu điểm 45 phút',
                          value=1, description='số lượng tối thiểu điểm 45 phút'))
    db.session.add(Policy(key='max_test45', name='số lượng tối đa điểm 45 phút',
                          value=3, description='số lượng tối đa điểm 45 phút'))

    db.session.add(Policy(key='final_test', name='số lượng điểm cuối kỳ',
                          value=1, description='số lượng điểm cuối kỳ'))

    db.session.add(Policy(key='min_success', name='điểm tối thiểu để đạt',
                          value=5, description='điểm tối thiểu để đạt'))

    db.session.add(Level(name='10', description='Khối 10', subject_names=[
                   'toán', 'văn', 'tiếng anh', 'sử', 'địa']))
    db.session.add(Level(name='11', description='Khối 11', subject_names=[
        'toán', 'văn', 'tiếng anh', 'sử', 'địa']))
    db.session.add(Level(name='12', description='Khối 12', subject_names=[
        'toán', 'văn', 'tiếng anh', 'sử', 'địa']))

    db.session.add(
        User(name='admin', email='admin@gmail.com', password=generage_password('password'), is_admin=True, is_teacher=True, is_staff=True))

    db.session.commit()


def generage_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()


if __name__ == '__main__':
    migrate()
