from .models import User


def check_login(email, password):
    return User.query.filter_by(email=email, password=password).first()
