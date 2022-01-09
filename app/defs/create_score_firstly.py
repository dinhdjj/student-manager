from flask import render_template
from flask_login import login_required, current_user

from ..models import Subject


@login_required
def create_score_firstly():

    subjects = Subject.query.filter_by(teacher_id=current_user.id).all()

    return render_template('page/create_score_firstly.html', subjects=subjects)
