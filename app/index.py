from . import app, is_debug


def run_app():
    app.run(debug=is_debug)


if __name__ == '__main__':
    run_app()
