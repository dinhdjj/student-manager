
from . import db
from .models import User, SubjectStudent


def check_login(email, password):
    return User.query.filter_by(email=email, password=password).first()


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
