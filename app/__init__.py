from flask import Flask
from .routes import define_routes
from dotenv import dotenv_values

config = dotenv_values(".env")
is_debug = config.get("APP_DEBUG", 'False') == 'True'

app = Flask(__name__)
app.secret_key = config.get('APP_SECRET_KEY', 'default')
define_routes(app)
