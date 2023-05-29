from flask import Flask

app = Flask(__name__)

from . import views
from .api import api

app.register_blueprint(api)
