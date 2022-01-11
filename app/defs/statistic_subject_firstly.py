from flask import render_template, request, redirect
from flask_login import login_required, current_user
from math import ceil

from ..models import Subject


@login_required
def statistic_subject_firstly():
    if(not current_user.is_admin):
        return render_template('page/403.html')

    page_size = 12
    page = request.args.get('page', 1, type=int)
    last_page = ceil(Subject.query.count() / page_size)
    start = (page - 1) * page_size
    end = start + page_size

    model_subjects = Subject.query.slice(start, end).all()

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
    return render_template('page/statistic_subject_firstly.html', subjects=subjects, last_page=last_page, page=page, range=range)


def find_subject(subjects, model_subject):
    for subject in subjects:
        if subject['name'] == model_subject.name:
            return subject
    return None
