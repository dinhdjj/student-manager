from flask import render_template, request, redirect
from flask_login import login_required, current_user

from app import db
from ..models import Policy


@login_required
def manage_policies():
    if(not current_user.is_admin):
        return render_template('page/403.html')

    errors = {}
    successes = {}

    max_amount_policy = Policy.query.filter_by(key='max_amount').first()
    min_age_policy = Policy.query.filter_by(key='min_age').first()
    max_age_policy = Policy.query.filter_by(key='max_age').first()

    if request.method == 'POST':
        max_amount = request.form.get('max_amount')
        min_age = request.form.get('min_age')
        max_age = request.form.get('max_age')

        if not max_amount:
            errors['max_amount'] = 'Số lượng học sinh tối đa một lớp là bắt buộc'
        if not min_age:
            errors['min_age'] = 'Tuổi nhập học tối thiểu là bắt buộc'
        if not max_age:
            errors['max_age'] = 'Tuổi nhập học tối đa là bắt buộc'

        if not errors:
            max_amount_policy.value = max_amount
            min_age_policy.value = min_age
            max_age_policy.value = max_age
            db.session.commit()
            successes['result'] = 'Cập nhật thành công'

    return render_template('page/manage_policies.html', max_amount_policy=max_amount_policy, min_age_policy=min_age_policy, max_age_policy=max_age_policy, errors=errors, successes=successes)
