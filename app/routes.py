from flask import render_template, request, redirect

from .defs.login import login
from .defs.logout import logout


def define_routes(app):
    @app.route('/')
    def index():
        return render_template('page/home.html')

    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout', methods=['POST'])(logout)
