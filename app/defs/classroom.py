import math

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import exc

from app import db
from app.defs.level import a
from app.models import Classroom, Level
from app.utils import add_or_update_c, count_c, get_level, get_class, check_c, delete_c, get_teacher, add_subject, \
    delete_subject, get_subject, update_subject


@login_required
def class_manage():
    if not current_user.is_teacher or not current_user.is_admin:
        return render_template('page/403.html')
    err = ''
    page = request.args.get('page', 1)
    l = get_level()
    c = get_class(page=int(page))
    if request.method == 'POST':
        kw = request.form.get('kw')
        c = get_class(kw=kw)
    return render_template('page/classroom.html',
                           c=c,
                           l=l,
                           err=err,
                           count=(math.ceil(count_c() / 4)))


def class_info():
    a = []
    class_id = request.args.get('id')
    cl = Classroom.query.get(class_id)
    info = enumerate(cl.students)
    return render_template('page/students_in_classroom.html', cl=cl, info=info)


def add_update_class():
    l = get_level()
    c = {}
    err = {}
    class_id = request.args.get('id', None)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        year = request.form.get('year')
        level = request.form.get('level')
        check = None
        if not class_id:
            check = check_c(name=name)
        if not name:
            err['name'] = 'Ten Khong duoc de trong'
        if not description:
            err['description'] = 'Mo ta Khong duoc de trong'
        if check:
            err['check'] = 'Ten da ton tai'
        if not err:
            add_or_update_c(class_id=class_id, name=name, description=description,year=year, level_id=level)
            return redirect(url_for('class_manage'))
    if class_id:
        c = Classroom.query.get(class_id)
    return render_template('page/add_class.html', l=l, c=c, err=err)

def delete_class():
    err = ''
    class_id = request.args.get('id', None)
    cl = Classroom.query.get(class_id)
    subject = cl.level.subject_names
    subject = a(subject=subject)
    subject = subject.split(',')
    try:
        for i in subject:
            name = i + " " + cl.name
            if get_subject(name=name):
                delete_subject(name=name)
        delete_c(class_id=class_id)
        err = 'Xoa Thanh Cong'
        redirect('/class/manage')
    except exc.IntegrityError:
        db.session.rollback()
        err = 'Co loi xay ra xoa khong thanh cong'
    return render_template('page/classroom.html', err=err)


def chose_teacher():
    class_id = request.args.get('id', None)
    t = get_teacher()
    cl = Classroom.query.get(class_id)
    subject = cl.level.subject_names
    subject = a(subject=subject)
    subject = subject.split(',')
    subject = enumerate(subject)
    if request.method == 'POST':
        for idx, i in subject:
            name = i + " " + cl.name
            description = 'Mon '+ i +' lop ' + cl.name
            classroom_id = cl.id
            c = str('teacher' + idx.__str__())
            teacher_id = request.form.get(c)
            s = get_subject(name=name)
            if not s:
                add_subject(name=name,description=description,classroom_id=classroom_id,teacher_id=teacher_id)
            else:
                update_subject(name=name,description=description,classroom_id=classroom_id,teacher_id=teacher_id)
        return redirect('/class/manage')
    return render_template('page/chose_teacher.html',cl=cl,subject=subject,teacher=t)
