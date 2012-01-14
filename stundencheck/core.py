from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

from stundencheck import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('SETTINGS', silent=True)

db = SQLAlchemy(app)
