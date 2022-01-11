from flask import Flask
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

config = dotenv_values(".env")
is_debug = config.get("APP_DEBUG", 'False') == 'True'

app = Flask(__name__)
app.secret_key = config.get('APP_SECRET_KEY', 'default')

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
    config.get('MYSQL_USER') + ':' + \
    quote(config.get('MYSQL_PASSWORD')) + '@' + config.get('MYSQL_HOST') + \
    ':' + config.get('MYSQL_PORT') + '/' + \
    config.get('MYSQL_DATABASE') + '?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



db = SQLAlchemy(app=app)
