from flask import render_template, request, redirect
from flask_login import login_required, current_user

from app import db
from ..models import Classroom, ClassroomStudent, Policy, Student


@login_required
def class_manage_students(class_id):
    if(not current_user.is_staff):
        return render_template('page/403.html')

    classroom = Classroom.query.get(class_id)
    if(not classroom):
        return render_template('page/404.html')

    errors = {}
    successes = {}

    if request.method == 'POST':
        student_ids = request.form.getlist('student_ids[]')
        if(not student_ids):
            errors['student_ids'] = 'Vui lòng chọn ít nhất 1 học sinh'

        max_amount_policy = Policy.query.filter_by(key="max_amount").first()
        current_student_amount = ClassroomStudent.query.filter_by(
            classroom_id=class_id).count()
        if(max_amount_policy.value < len(student_ids) + current_student_amount):
            errors['student_ids'] = f'Số lượng học sinh vượt quá giới hạn cho phép ({max_amount_policy.value})'

        if(not errors):
            count = 0
            for student_id in student_ids:
                student = Student.query.get(student_id)
                if(student):
                    db.session.add(ClassroomStudent(student_id=student.id,
                                                    classroom_id=classroom.id))
                    count += 1
            db.session.commit()
            successes['result'] = f"Đã thêm thành công {count} học sinh vào lớp"

    students = classroom.students
    unadded_students = Student.query.filter(
        Student.id.not_in(get_student_ids(students))).all()

    return render_template('page/class_manage_students.html', classroom=classroom, students=students, errors=errors, successes=successes, unadded_students=unadded_students)


def get_student_ids(students):
    student_ids = []
    for student in students:
        student_ids.append(student.id)
    return student_ids
