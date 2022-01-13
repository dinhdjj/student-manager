import hashlib

from . import db
from .models import User, SubjectStudent, Subject, Classroom, Level, generage_password


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


def get_level(name=None, kw=None, page=1):
    level = Level.query
    if name:
        level = Level.query.filter(Level.name.__eq__(name))
    if kw:
        level = Level.query.filter(Level.name.__eq__(kw))
    page_size = 4
    start = (page - 1) * page_size
    end = start + page_size
    return level.slice(start, end).all()


def add_or_upadate_l(level_id=None, name=None, description=None, subject_names=None):
    if level_id:
        lv = Level.query.get(level_id)
        lv.name = name
        lv.description = description
        lv.subject_names = subject_names
        db.session.add(lv)
        db.session.commit()
    else:
        lv = Level(name=name, description=description, subject_names=subject_names)
        db.session.add(lv)
        db.session.commit()


def delete_l(level_id):
    lv = Level.query.get(level_id)
    db.session.delete(lv)
    db.session.commit()


def count_l():
    if Level.query.count() == 0:
        return 0
    return Level.query.count()


def check_l(name):
    return Level.query.filter(Level.name.__eq__(name)).first()


# ClassRoom
def check_c(name):
    return Classroom.query.filter(Classroom.name.__eq__(name)).first()


def count_c():
    if Classroom.query.count() == 0:
        return 0
    return Classroom.query.count()


def add_or_update_c(class_id=None, name=None, description=None, year=None, level_id=None):
    if class_id:
        cl = Classroom.query.get(class_id)
        cl.name = name
        cl.description = description
        cl.year = year
        cl.level_id = level_id
        db.session.add(cl)
        db.session.commit()
    else:
        cl = Classroom(name=name, description=description, year=year, level_id=level_id)
        db.session.add(cl)
        db.session.commit()


def delete_c(class_id):
    c = Classroom.query.get(class_id)
    db.session.delete(c)
    db.session.commit()


def get_class(level_id=None, kw=None, page=1):
    cl = Classroom.query
    if kw:
        cl = Classroom.query.filter(Classroom.name.__eq__(kw))
    if level_id:
        cl = Classroom.query.filter(Classroom.level_id.__eq__(level_id))
    page_size = 4
    start = (page - 1) * page_size
    end = start + page_size
    return cl.slice(start, end).all()


def add_subject(name, description, classroom_id, teacher_id):
    s = Subject(name=name, description=description, classroom_id=classroom_id, teacher_id=teacher_id)
    db.session.add(s)
    db.session.commit()


def delete_subject(name):
    subject = Subject.query.filter(Subject.name.__eq__(name)).first()
    db.session.delete(subject)
    db.session.commit()


def get_subject(name):
    subject = Subject.query.filter(Subject.name.__eq__(name)).first()
    return subject


def update_subject(name, description, classroom_id, teacher_id):
    subject = Subject.query.filter(Subject.name.__eq__(name)).first()
    subject.name = name
    subject.description = description
    subject.classroom_id = classroom_id
    subject.teacher_id = teacher_id
    db.session.add(subject)
    db.session.commit()


def get_teacher():
    t = User.query.filter(User.is_teacher.__eq__(True)).all()
    return t
