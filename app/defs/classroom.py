from flask import render_template, request, redirect
from app import db
from app.models import Classroom


def class_room():
    c = Classroom.query.all()
    return render_template('page/classroom.html', c=c)


def class_info():
    a = []
    class_id = request.args.get('id')
    cl = Classroom.query.get(class_id)
    info = enumerate(cl.students)
    return render_template('page/students_in_classroom.html',cl=cl, info=info)

