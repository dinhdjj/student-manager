from os import name
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from . import app, db
from .models import SubjectStudent, User, Classroom, Subject, Student, Policy, Level, ClassroomStudent


class AdminView(ModelView):
    def is_accessible(self):
        return True


class TeacherView(ModelView):
    def is_accessible(self):
        return True


class StaffView(ModelView):
    def is_accessible(self):
        return True


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return 'index admin'


admin = Admin(app=app,
              name="Hệ thống quản lý học sinh",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AdminView(User, db.session, name='Người dùng'))
admin.add_view(AdminView(Policy, db.session, name='Chính sách'))
admin.add_view(AdminView(Level, db.session, name="Khối lớp"))
admin.add_view(AdminView(Subject, db.session, name="Môn học"))

admin.add_view(TeacherView(SubjectStudent, db.session, name='Điểm số',))

admin.add_view(StaffView(Classroom, db.session, name='Lớp học'))
admin.add_view(StaffView(Student, db.session, name='Học sinh'))
admin.add_view(StaffView(ClassroomStudent,
               db.session, name='Lớp học - Học sinh'))
