from flask import Flask
from config import Config
from flask_session import Session


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'6hc/_gsh,./;2ZZx3c6_s,1//'
Session(app)

from app import routes