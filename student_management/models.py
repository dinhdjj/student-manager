from sqlalchemy import Column, Integer, String, Float, ForeignKey
from student_management import db


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(Integer, nullable=False)


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(Integer, nullable=False)

if __name__ == '__main__':
    db.create_all()
