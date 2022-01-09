from flask import render_template, request, redirect
from flask_login import login_required, current_user

from ..models import Subject


@login_required
def statistic_subject_firstly():
    if(not current_user.is_admin):
        return render_template('page/403.html')

    model_subjects = Subject.query.all()

    subjects = []
    for model_subject in model_subjects:
        subject = find_subject(subjects, model_subject)
        if subject:
            subjects.remove(subject)
        if not subject:
            subject = {
                'name': model_subject.name,
                'years': []
            }

        year = model_subject.classroom.year
        if(year not in subject['years']):
            subject['years'].append(year)

        subjects.append(subject)

    print(subjects)
    return render_template('page/statistic_subject_firstly.html', subjects=subjects)


def find_subject(subjects, model_subject):
    for subject in subjects:
        if subject['name'] == model_subject.name:
            return subject
    return None
