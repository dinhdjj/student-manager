from app import db
from app.models import Classroom, ClassroomStudent, Level, Student, Subject, User
from app.utils import generage_password
import string
import random


def create_user(name, role, email):
    password = generage_password('password')
    is_admin = False
    is_teacher = False
    is_staff = False
    if role == 'admin':
        is_admin = True
    elif role == 'teacher':
        is_teacher = True
    elif role == 'staff':
        is_staff = True
    user = User(name=name, email=email, password=password,
                is_admin=is_admin, is_teacher=is_teacher, is_staff=is_staff)

    db.session.add(user)
    db.session.commit()
    return user


def create_student(name):
    phone_number = '0'.join(random.choice(string.digits) for i in range(8))
    email = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    address = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    birth_date = '2000-01-01'
    gender = 'male'

    student = Student(name=name, phone_number=phone_number, email=email,
                      address=address, birth_date=birth_date, gender=gender)
    db.session.add(student)
    db.session.commit()
    return student


def create_classroom(name, year, level_id):
    description = ''.join(random.choice(string.ascii_lowercase)
                          for i in range(10))
    classroom = Classroom(name=name, description=description,
                          level_id=level_id, year=year)
    db.session.add(classroom)
    db.session.commit()
    return classroom


def create_subject(name, teacher_id, classroom_id):
    description = ''.join(random.choice(string.ascii_lowercase)
                          for i in range(10))
    subject = Subject(name=name, description=description,
                      teacher_id=teacher_id, classroom_id=classroom_id)
    db.session.add(subject)
    db.session.commit()
    return subject


if __name__ == '__main__':
    level10 = Level.query.filter_by(name='10').first()
    level11 = Level.query.filter_by(name='11').first()
    level12 = Level.query.filter_by(name='12').first()

    teacher1 = create_user('Teacher 1', 'teacher', 'teacher1@gmail.com')
    teacher2 = create_user('Teacher 2', 'teacher', 'teacher2@gmail.com')
    teacher3 = create_user('Teacher 2', 'teacher', 'teacher3@gmail.com')

    student1 = create_student('Student 1')
    student2 = create_student('Student 2')
    student3 = create_student('Student 3')
    student4 = create_student('Student 4')
    student5 = create_student('Student 5')
    student6 = create_student('Student 6')
    student7 = create_student('Student 7')
    student8 = create_student('Student 8')

    classroom12021 = create_classroom('lớp 10 - 1 - 2021', 2021, level10.id)
    classroom22021 = create_classroom('lớp 11 - 2 - 2021', 2021, level11.id)
    classroom32021 = create_classroom('lớp 12 - 3 - 2021', 2021, level12.id)

    db.session.add(ClassroomStudent(
        classroom_id=classroom12021.id, student_id=student1.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22021.id, student_id=student1.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32021.id, student_id=student1.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom12021.id, student_id=student2.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22021.id, student_id=student2.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32021.id, student_id=student2.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom12021.id, student_id=student3.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22021.id, student_id=student3.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32021.id, student_id=student3.id))

    classroom12020 = create_classroom('lớp 10 - 1 - 2020', 2020, level10.id)
    classroom22020 = create_classroom('lớp 11 - 2 - 2020', 2020, level11.id)
    classroom32020 = create_classroom('lớp 12 - 3 - 2020', 2020, level12.id)

    db.session.add(ClassroomStudent(
        classroom_id=classroom12020.id, student_id=student4.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22020.id, student_id=student4.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32020.id, student_id=student4.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom12020.id, student_id=student5.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22020.id, student_id=student5.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32020.id, student_id=student5.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom12020.id, student_id=student6.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22020.id, student_id=student6.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32020.id, student_id=student6.id))

    classroom12019 = create_classroom('lớp 10 - 1 - 2019', 2019, level10.id)
    classroom22019 = create_classroom('lớp 11 - 2 - 2019', 2019, level11.id)
    classroom32019 = create_classroom('lớp 12 - 3 - 2019', 2019, level12.id)

    db.session.add(ClassroomStudent(
        classroom_id=classroom12019.id, student_id=student7.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom22019.id, student_id=student7.id))
    db.session.add(ClassroomStudent(
        classroom_id=classroom32019.id, student_id=student8.id))

    subject12021 = create_subject('Toán', teacher1.id, classroom12021.id)
    subject22021 = create_subject('Lý', teacher2.id, classroom22021.id)
    subject32021 = create_subject('Hóa', teacher3.id, classroom32021.id)

    subject12020 = create_subject('Toán', teacher1.id, classroom12020.id)
    subject22020 = create_subject('Lý', teacher2.id, classroom22020.id)
    subject32020 = create_subject('Hóa', teacher3.id, classroom32020.id)

    subject12019 = create_subject('Toán', teacher1.id, classroom12019.id)
    subject22019 = create_subject('Lý', teacher2.id, classroom22019.id)
    subject32019 = create_subject('Hóa', teacher3.id, classroom32019.id)
