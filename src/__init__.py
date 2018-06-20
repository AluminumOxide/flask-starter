from flask import Flask
from src.database import Database

app = Flask('FlaskStarter')
db = Database(app).db
