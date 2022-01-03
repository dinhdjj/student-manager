from flask import render_template, request, redirect
from sqlalchemy import exc

from app import db
from app.models import Level
from app.levelmanage import add_or_upadate, delete
from .classroom import get_class


def level_manage(err=''):
    l = Level.query.all()
    level = enumerate(l)
    c = get_class()
    return render_template('page/level.html', level=level, c=c, err=err)


def add_or_update_level():
    level_id = request.args.get('id', None)
    l = {}
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        add_or_upadate(lid=level_id, name=name, description=description)
        return redirect('/level/manage')
    if level_id:
        l = Level.query.get(level_id)
    return render_template('page/add_level.html', level=l)


def delete_level():
    err = ''
    level_id = request.args.get('id', None)
    try:
        delete(level_id=level_id)
        err = 'Xoa Thanh Cong'
        redirect('/level/manage')
    except exc.IntegrityError:
        db.session.rollback()
        err = 'Co loi xay ra xoa khong thanh cong'
    return render_template('page/level.html', err=err)


def get_level():
    l = Level.query.all()
    return l
