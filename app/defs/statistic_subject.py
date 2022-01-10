from flask import render_template
from flask_login import login_required

from ..models import Policy, Subject, SubjectStudent


@login_required
def statistic_subject(subject_name, semester, year):
    subjects = Subject.query.filter_by(name=subject_name).filter(
        Subject.classroom.has(year=year)).all()

    if(semester != 1 and semester != 2):
        return render_template('page/404.html')

    if(not len(subjects)):
        return render_template('page/404.html')

    min_success_policy = Policy.query.filter_by(key='min_success').first()
    statistics = []
    for subject in subjects:
        classroom = subject.classroom
        students = classroom.students
        statistic = {
            "classroom": classroom.name,
            "amount": len(students),
            "success": 0,
            "fail": 0,
        }

        for student in students:
            subject_student = SubjectStudent.query.filter_by(
                student_id=student.id,
                subject_id=subject.id,
            ).first()

            s1_sum = 0
            s1_coefficient = 0
            s2_sum = 0
            s2_coefficient = 0

            if(subject_student):
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

            if semester == 1:
                if(s1_coefficient == 0):
                    pass
                elif(s1_sum / s1_coefficient >= min_success_policy.value):
                    statistic['success'] += 1
                else:
                    statistic['fail'] += 1
            else:
                if(s2_coefficient == 0):
                    pass
                elif(s2_sum / s2_coefficient >= min_success_policy.value):
                    statistic['success'] += 1
                else:
                    statistic['fail'] += 1

        statistics.append(statistic)

    return render_template('page/statistic_subject.html', statistics=statistics, year=year, semester=semester, round=round, subject_name=subject_name)
