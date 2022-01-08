from flask import render_template, request
from flask_login import current_user, login_required

from app import db
from app.models import Classroom, Subject
from app.utils import get_or_create_student_subjects, listToString


@login_required
def create_score(class_id, subject_id, semester):
    if(semester != 1 and semester != 2):
        return render_template('page/404.html')

    if(current_user.is_teacher == False):
        return render_template('page/403.html')

    errors = {}
    successes = {}
    classroom = Classroom.query.get(class_id)
    subject = Subject.query.get(subject_id)

    if(not classroom or not subject):
        return render_template('page/404.html')

    is_exist = subject.classroom_id == classroom.id
    if(not is_exist):
        return render_template('page/404.html')

    if(subject.teacher_id != current_user.id):
        return render_template('page/403.html')

    semester = 's' + str(semester)
    students = classroom.students
    sss = get_or_create_student_subjects(students, subject)

    if(request.method == 'POST'):
        form = request.form
        for ss in sss:
            test15 = parse_scores(form.get(f"scores[{ss.id}][test15]"))
            test45 = parse_scores(form.get(f"scores[{ss.id}][test45]"))
            final_test = form.get(f"scores[{ss.id}][final_test]")
            if final_test:
                final_test = float(final_test)

            setattr(ss, semester + '_test15', test15)
            setattr(ss, semester + '_test45', test45)
            if final_test:
                setattr(ss, semester + '_final_test', final_test)
            db.session.add(ss)
        db.session.commit()
        successes['result'] = 'Lưu thành công'

    return render_template('page/create_score.html', errors=errors, successes=successes, classroom=classroom, subject=subject, students=students, sss=sss, listToString=listToString, semester=semester)


def parse_scores(string):
    scores = string.split(',')
    scores = [x for x in scores if x]
    return [float(score) for score in scores]
