from flask import render_template, request
from flask_login import current_user, login_required

from app import db
from app.models import Classroom, Policy, Subject
from app.utils import get_or_create_student_subjects, listToString


@login_required
def create_score(subject_id, semester):
    if(semester != 1 and semester != 2):
        return render_template('page/404.html')

    if(current_user.is_teacher == False):
        return render_template('page/403.html')

    errors = {}
    successes = {}
    subject = Subject.query.get(subject_id)

    if(subject.teacher_id != current_user.id):
        return render_template('page/403.html')

    semester = 's' + str(semester)
    students = subject.classroom.students
    sss = get_or_create_student_subjects(students, subject)
    min_test15_policy = Policy.query.filter_by(key='min_test15').first()
    max_test15_policy = Policy.query.filter_by(key='max_test15').first()
    min_test45_policy = Policy.query.filter_by(key='min_test45').first()
    max_test45_policy = Policy.query.filter_by(key='max_test45').first()
    final_test_policy = Policy.query.filter_by(key='final_test').first()

    if(request.method == 'POST'):
        form = request.form
        for ss in sss:
            test15 = parse_scores(form.get(f"scores[{ss.id}][test15]"))
            test45 = parse_scores(form.get(f"scores[{ss.id}][test45]"))
            final_test = form.get(f"scores[{ss.id}][final_test]")
            if final_test:
                final_test = float(final_test)

            if len(test15) < min_test15_policy.value:
                errors[f"scores[{ss.id}][test15]"] = f"Số lượng điểm thi 15 phút phải lớn hơn hoặc bằng {min_test15_policy.value}"
            elif len(test15) > max_test15_policy.value:
                errors[f"scores[{ss.id}][test15]"] = f"Số lượng điểm thi 15 phút phải nhỏ hơn hoặc bằng {max_test15_policy.value}"
            if len(test45) < min_test45_policy.value:
                errors[f"scores[{ss.id}][test45]"] = f"Số lượng điểm thi 15 phút phải lớn hơn hoặc bằng {min_test45_policy.value}"
            elif len(test45) > max_test45_policy.value:
                errors[f"scores[{ss.id}][test45]"] = f"Số lượng điểm thi 15 phút phải nhỏ hơn hoặc bằng {max_test45_policy.value}"
            if not isinstance(final_test, float):
                errors[f"scores[{ss.id}][final_test]"] = f"Điểm thi cuối kỳ là bắt buộc"

            setattr(ss, semester + '_test15', test15)
            setattr(ss, semester + '_test45', test45)
            if isinstance(final_test, float):
                setattr(ss, semester + '_final_test', final_test)
            db.session.add(ss)

        if not errors:
            db.session.commit()
            successes['result'] = 'Lưu thành công'

    return render_template('page/create_score.html', errors=errors, successes=successes, subject=subject, students=students, sss=sss, listToString=listToString, semester=semester, str=str, max_test15_policy=max_test15_policy, min_test15_policy=min_test15_policy, max_test45_policy=max_test45_policy, min_test45_policy=min_test45_policy, final_test_policy=final_test_policy)


def parse_scores(string):
    scores = string.split(',')
    scores = [x for x in scores if x]
    return [float(score) for score in scores]
