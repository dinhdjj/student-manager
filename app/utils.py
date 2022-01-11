import hashlib

from . import db
from .models import User, SubjectStudent


def check_login(email, password):
    user = User.query.filter_by(email=email).first()
    if check_password(password, user.password):
        return user
    return None


def generage_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()


def check_password(checked_password, password):
    return generage_password(checked_password) == password


def get_or_create_student_subjects(students, subject):
    student_subjects = []

    for student in students:
        ss = SubjectStudent.query.filter_by(
            student_id=student.id, subject_id=subject.id).first()
        if not ss:
            ss = SubjectStudent(student_id=student.id, subject_id=subject.id)
            db.session.add(ss)
        student_subjects.append(ss)

    db.session.commit()
    return student_subjects


def listToString(s, delimiter=','):
    result = ""
    for i in s:
        result += str(i) + delimiter
    return result[:-1]
