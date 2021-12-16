from flask import Flask
from .routes import define_routes

app = Flask(__name__)
app.secret_key = '%^&*()GhjkkVBNMFGY#$%^&*)(*&^456789876'

define_routes(app)
