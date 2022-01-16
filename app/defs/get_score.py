from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import null

from ..models import Classroom


@login_required
def get_score(classroom_id):
    if(not current_user.is_teacher):
        return render_template('page/403.html')

    classroom = Classroom.query.get(classroom_id)
    if(not classroom):
        return render_template('page/404.html')

    students = classroom.students
    scores = []
    for student in students:
        score = {
            'name': student.name,
            "s1": None,
            "s2": None,
        }
        s1_sum = 0
        s1_coefficient = 0
        s2_sum = 0
        s2_coefficient = 0
        for subject_student in student.subject_students:
            if(subject_student.s1_test15):
                for test in subject_student.s1_test15:
                    s1_sum += test
                    s1_coefficient += 1
            if(subject_student.s1_test45):
                for test in subject_student.s1_test45:
                    s1_sum += test * 2
                    s1_coefficient += 2
            if(subject_student.s1_final_test):
                s1_sum += subject_student.s1_final_test * 3
                s1_coefficient += 3

            if(subject_student.s2_test15):
                for test in subject_student.s2_test15:
                    s2_sum += test
                    s2_coefficient += 1
            if(subject_student.s2_test45):
                for test in subject_student.s2_test45:
                    s2_sum += test * 2
                    s2_coefficient += 2
            if(subject_student.s2_final_test):
                s2_sum += subject_student.s2_final_test * 3
                s2_coefficient += 3

        score['s1'] = round(s1_sum /
                            s1_coefficient, 2) if s1_coefficient else 'Chưa có điểm'
        score['s2'] = round(s2_sum /
                            s2_coefficient, 2) if s2_coefficient else 'Chưa có điểm'
        scores.append(score)

    return render_template('page/score.html', scores=scores, classroom=classroom)
