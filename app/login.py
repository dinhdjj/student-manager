from flask_login import LoginManager

from .models import User


def use_flask_login(app):
    login = LoginManager(app=app)

    @login.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(user_id)

    return login
