from . import app, is_debug
from .admin import *


def run_app():
    app.run(debug=is_debug)


if __name__ == '__main__':
    run_app()
