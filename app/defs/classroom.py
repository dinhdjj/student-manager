from flask import render_template, request, redirect, url_for
from app import db
from app.models import Classroom, Level
from app.classmanage import add, update


def class_room():
    l = Level.query.all()
    c = Classroom.query.all()
    return render_template('page/classroom.html', c=c, l=l)


def class_info():
    a = []
    class_id = request.args.get('id')
    cl = Classroom.query.get(class_id)
    info = enumerate(cl.students)
    return render_template('page/students_in_classroom.html', cl=cl, info=info)


def add_class():
    l = Level.query.all()
    c = {}
    class_id = request.args.get('id',None)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        level= request.form.get('level',0)
        if class_id:
            update(id=class_id, name=name,description=description,level_id=level)
        else:
            add(name=name,description=description,level_id=level )
        return redirect(url_for('class_room'))
    if class_id:
        c = Classroom.query.get(class_id)
    return render_template('page/add_class.html', l=l, c=c)


def get_class():
    c = Classroom.query.all()
    return c
