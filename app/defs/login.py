from flask import render_template, request, redirect
from flask_login import login_user

from ..utils import check_login


def login():
    errors = {}

    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']

        if(not email):
            errors['email'] = 'Địa chỉ email là bắt buộc.'
        if(not password):
            errors['password'] = 'Mật khẩu là bắt buộc.'

        if(not errors):
            user = check_login(email, password)
            if(user):
                login_user(user=user)
                return redirect('/')
            else:
                errors['result'] = 'Đăng nhập không thành công.'

    return render_template('page/login.html', errors=errors)
