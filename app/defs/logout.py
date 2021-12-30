from flask import redirect
from flask_login import logout_user


def logout():
    logout_user()
    return redirect('/')
