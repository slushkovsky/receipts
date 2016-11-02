from flask import Flask

from . import config

app = Flask(__name__)

from .routes import bp 

app.register_blueprint(bp)
