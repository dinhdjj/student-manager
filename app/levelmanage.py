from .models import Level
from . import db


def add_or_upadate(lid=None ,name=None, description=None):
    if lid:
        lv = Level.query.get(lid)
        lv.name = name
        lv.description = description
        db.session.add(lv)
        db.session.commit()
    else:
        lv = Level(name=name, description=description)
        db.session.add(lv)
        db.session.commit()


def delete(level_id):
    lv = Level.query.get(level_id)
    db.session.delete(lv)
    db.session.commit()




