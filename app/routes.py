from flask import render_template


def define_routes(app):
    @app.route('/')
    def index():
        return render_template('page/home.html')
