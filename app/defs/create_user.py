from flask import render_template, request, redirect
from flask_login import login_required, current_user

from app import db
from ..models import User
from ..utils import generage_password


@login_required
def create_user():
    if(not current_user.is_admin):
        return render_template('page/403.html')

    errors = {}
    successes = {}

    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmed_password')
        roles = request.form.getlist('roles[]')
        if not roles:
            roles = []

        if(not name):
            errors['name'] = 'Tên là bắt buộc'
        if(not email):
            errors['email'] = 'Email là bắt buộc'
        elif(User.query.filter_by(email=email).first()):
            errors['email'] = 'Email đã tồn tại trên hệ thống'
        if(not password):
            errors['password'] = 'Mật khẩu là bắt buộc'
        if(not confirmed_password):
            errors['confirmed_password'] = 'Xác nhận mật khẩu là bắt buộc'
        if(password != confirmed_password):
            errors['confirmed_password'] = 'Xác nhận mật khẩu không chính xác'
        if(not roles):
            errors['roles[]'] = 'Phải nắm dữ ít nhất một vai trò'

        if not errors:
            is_admin = False
            if 'admin' in roles:
                is_admin = True
            is_teacher = False
            if 'teacher' in roles:
                is_teacher = True
            is_staff = False
            if 'staff' in roles:
                is_staff = True
            user = User(name=name, email=email,
                        password=generage_password(password), is_admin=is_admin, is_teacher=is_teacher, is_staff=is_staff)
            db.session.add(user)
            db.session.commit()
            successes['result'] = 'Thêm thành công'

    return render_template('page/create_user.html', errors=errors, successes=successes)
