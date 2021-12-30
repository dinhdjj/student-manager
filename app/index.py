from . import app, is_debug
from .admin import *
from .login import use_flask_login
from .routes import define_routes

define_routes(app)
login = use_flask_login(app)


def run_app():
    app.run(debug=is_debug)


if __name__ == '__main__':
    run_app()
