import json
import math

from flask import render_template, request, redirect
from flask_login import current_user, login_required
from sqlalchemy import exc

from app import db
from app.models import Level
from app.utils import add_or_upadate_l, delete_l, get_level, count_l, get_class, check_l


@login_required
def level_manage():
    err = ''
    if not current_user.is_staff:
        return render_template('page/403.html')
    page = request.args.get('page', 1)
    c = get_class()
    count = count_l()
    l = get_level(page=int(page))
    if request.method == 'POST':
        kw = request.form.get('kw', None)
        l = get_level(kw=kw)
    level = enumerate(l)
    return render_template('page/level.html', level=level, c=c, err=err, count=(math.ceil(count / 4)))


def add_or_update_level():
    err = {}
    subject = ''
    level_id = request.args.get('id', None)
    l = {}
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        subject = parse_subject(request.form.get('subject'))
        subject_names = json.dumps(subject)
        check = check_l(name=name)
        if not level_id:
            if not name:
                err['name'] = 'Ten khong duoc de trong'
            if not description:
                err['description'] = 'Mo ta khong duoc de trong'
            if not subject_names:
                err['subject'] = 'Hay nhap cac mon hoc Vd: Toan, Van'
            if check:
                err['check'] = 'Ten da ton tai'
        if not err:
            add_or_upadate_l(level_id=level_id, name=name, description=description, subject_names=subject_names)
            return redirect('/level/manage')
    if level_id:
        l = Level.query.get(level_id)
        subjects = l.subject_names
        subject = a(subject=subjects)
    return render_template('page/add_level.html', level=l, err=err, subject=subject)


def delete_level():
    err = ''
    level_id = request.args.get('id', None)
    try:
        delete_l(level_id=level_id)
        err = 'Xoa Thanh Cong'
        redirect('/level/manage')
    except exc.IntegrityError:
        db.session.rollback()
        err = 'Co loi xay ra xoa khong thanh cong'
    return render_template('page/level.html', err=err)


def parse_subject(string):
    subjects = string.replace(" ", '')
    subject = subjects.split(',')
    s = [x for x in subject if x]
    return s


def a(subject):
    a = subject.replace('[', '')
    a = a.replace(']', '')
    a = a.replace('"', '')
    a = a.replace(' ', '')
    return a
