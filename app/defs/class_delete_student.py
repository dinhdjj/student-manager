from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from ..models import Classroom, ClassroomStudent, Student


@login_required
def class_delete_student(class_id, student_id):
    if(not current_user.is_staff):
        return render_template('page/403.html')

    classroom_student = ClassroomStudent.query.filter_by(
        classroom_id=class_id, student_id=student_id).first()
    if(not classroom_student):
        return render_template('page/404.html')

    db.session.delete(classroom_student)
    db.session.commit()
    return redirect(url_for('class_manage_students', class_id=class_id))
