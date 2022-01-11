from flask import render_template, request, redirect

from .defs.login import login
from .defs.logout import logout
from .defs.level import level_manage, add_or_update_level, delete_level
from .defs.classroom import class_room, class_info, add_class
from .defs.change_password import change_password
from .defs.create_student import create_student
from .defs.create_score import create_score
from .defs.get_score import get_score
from .defs.statistic_subject import statistic_subject
from .defs.create_score_firstly import create_score_firstly
from .defs.statistic_subject_firstly import statistic_subject_firstly
from .defs.manage_policies import manage_policies
from .defs.create_user import create_user


def define_routes(app):
    @app.route('/')
    def index():
        return render_template('page/home.html')

    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout', methods=['POST'])(logout)
    app.route('/level/manage')(level_manage)
    app.route('/level/add', methods=['GET', 'POST'])(add_or_update_level)
    app.route('/level/delete', methods=['GET', 'POST'])(delete_level)
    app.route('/class/manage')(class_room)
    app.route('/class/students')(class_info)
    app.route('/class/add', methods=['GET', 'POST'])(add_class)

    app.route('/change_password', methods=['GET', 'POST'])(change_password)

    app.route('/student/create', methods=['GET', 'POST'])(create_student)

    app.route('/create-score', methods=['GET'])(create_score_firstly)
    app.route('/create-score/<int:subject_id>/<int:semester>',
              methods=['GET', 'POST'])(create_score)

    app.route('/scores/<classroom_id>', methods=['GET'])(get_score)

    app.route('/statistic-subject', methods=['GET'])(statistic_subject_firstly)
    app.route('/statistic-subject/<subject_name>/<int:semester>/<int:year>',
              methods=['GET'])(statistic_subject)

    app.route('/policies', methods=['GET', 'POST'])(manage_policies)

    app.route('/users/create', methods=['GET', 'POST'])(create_user)
