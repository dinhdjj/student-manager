from flask import render_template, request
from flask_login import login_required, current_user
from math import ceil

from ..models import Subject


@login_required
def create_score_firstly():
    if(not current_user.is_teacher):
        return render_template('page/403.html')

    page_size = 12
    page = request.args.get('page', 1, type=int)
    last_page = ceil(Subject.query.filter_by(
        teacher_id=current_user.id).count() / page_size)
    start = (page - 1) * page_size
    end = start + page_size

    subjects = Subject.query.filter_by(
        teacher_id=current_user.id).slice(start, end).all()

    return render_template('page/create_score_firstly.html', subjects=subjects, page=page, last_page=last_page, range=range)
