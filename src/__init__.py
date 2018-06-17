from flask import Flask
from src.database import Database

app = Flask('FlaskStarter')
db = Database(app).db

def create_app(test_config=None):

    from src.models.user import User
    db.clear()
    
    from src.controllers.auth import auth
    app.register_blueprint(auth.bp)
    
    from src.controllers import account
    app.register_blueprint(account.bp)

create_app()
