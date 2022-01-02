from flask import render_template, request, redirect

from .defs.login import login
from .defs.logout import logout
from .defs.level import level_manage, add_or_update_level,delete_level
from .defs.classroom import class_room,class_info


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
