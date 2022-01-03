from . import db
from .models import Classroom


def add(name, description, level_id):
    if name != '' and description != '':
        c = Classroom(name=name, description=description, level_id=level_id)
        db.session.add(c)
        db.session.commit()


def update(id, name, description, level_id):
    if name != '' and description != '':
        c = Classroom.query.get(id)
        c.name = name
        c.description = description
        c.level_id = level_id
        db.session.add(c)
        db.session.commit()

def delete(id):
    c = Classroom.query.get(id)
    db.session.remove(c)
    db.session.commit()
