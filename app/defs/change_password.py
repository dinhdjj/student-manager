from flask import render_template, request
from flask_login import login_required, current_user
from app import db
from app.utils import check_password, generage_password


@login_required
def change_password():
    errors = {}
    successes = {}

    if(request.method == 'POST'):
        old_password = request.form['old_password']
        password = request.form['password']
        confirmed_password = request.form['confirmed_password']

        if(not old_password):
            errors['old_password'] = 'Mật khẩu cũ là bắt buộc.'
        if(not password):
            errors['password'] = 'Mật khẩu mới là bắt buộc.'
        if(not confirmed_password):
            errors['confirmed_password'] = 'Mật khẩu xác nhận là bắt buộc.'

        if(password != confirmed_password):
            errors['confirmed_password'] = 'Mật khẩu xác nhận không khớp.'

        if(check_password(old_password, current_user.password)):
            errors['old_password'] = 'Mật khẩu cũ không chính xác.'

        if(not errors):
            current_user.password = generage_password(password)
            db.session.add(current_user)
            db.session.commit()
            successes['result'] = 'Đổi mật khẩu thành công.'

    return render_template('page/change_password.html', errors=errors, successes=successes)
