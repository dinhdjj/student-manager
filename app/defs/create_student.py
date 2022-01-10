from math import ceil
from flask import request
from flask.templating import render_template
from flask_login import login_required, current_user
from datetime import datetime

from ..models import Policy, Student
from app import db


@login_required
def create_student():
    if(current_user.is_staff == False):
        return render_template('page/403.html')

    errors = {}
    successes = {}

    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        birth_date = request.form.get('birth_date')
        gender = request.form.get('gender')

        if(not name):
            errors['name'] = 'Tên học sinh là bắt buộc'
        if(not email):
            errors['email'] = 'Địa chỉ email là bắt buộc'
        if(not phone):
            errors['phone'] = 'Số điện thoại là bắt buộc'
        if(not address):
            errors['address'] = 'Địa chỉ là bắt buộc'
        if(not birth_date):
            errors['birth_date'] = 'Ngày sinh là bắt buộc'
        else:
            age = (datetime.now() - datetime.strptime(birth_date, "%Y-%m-%d")).days
            age = ceil(age / 365)
            print(age)
            min_age_policy = Policy.query.filter_by(key='min_age').first()
            max_age_policy = Policy.query.filter_by(key='max_age').first()
            if(age < min_age_policy.value):
                errors['birth_date'] = 'Tuổi học sinh phải lớn hơn hoặc bằng ' + \
                    str(min_age_policy.value)
            if(age > max_age_policy.value):
                errors['birth_date'] = 'Tuổi học sinh phải nhỏ hơn hoặc bằng ' + \
                    str(max_age_policy.value)

        if(not gender):
            errors['gender'] = 'Gới tính là bắt buộc'

        if(not errors):
            student = Student(name=name, email=email, phone_number=phone,
                              address=address, birth_date=birth_date, gender=gender)
            db.session.add(student)
            db.session.commit()
            successes['result'] = 'Tiếp nhận thành công học sinh'

    return render_template('page/create_student.html', errors=errors, successes=successes)
