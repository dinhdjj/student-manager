from flask import render_template, request

from app import db
from app.models import Classroom, Subject
from app.utils import get_or_create_student_subjects, listToString


def create_score(class_id, subject_id):
    errors = {}
    successes = {}
    classroom = Classroom.query.get(class_id)
    subject = Subject.query.get(subject_id)

    if(not classroom or not subject):
        return render_template('page/404.html')

    is_exist = subject.level_id == classroom.level_id
    if(not is_exist):
        return render_template('page/404.html')

    students = classroom.students
    sss = get_or_create_student_subjects(students, subject)

    if(request.method == 'POST'):
        form = request.form
        for ss in sss:
            test15 = parse_scores(form.get(f"scores[{ss.id}][test15]"))
            test45 = parse_scores(form.get(f"scores[{ss.id}][test45]"))
            final_test = form.get(f"scores[{ss.id}][final_test]")
            if final_test:
                final_test = int(final_test)

            ss.test15 = test15
            ss.test45 = test45
            if final_test:
                ss.final_test = final_test
            db.session.add(ss)
        db.session.commit()
        successes['result'] = 'Lưu thành công'

    return render_template('page/create_score.html', errors=errors, successes=successes, classroom=classroom, subject=subject, students=students, sss=sss, listToString=listToString)


def parse_scores(string):
    scores = string.split(',')
    scores = [x for x in scores if x]
    return [int(score) for score in scores]
