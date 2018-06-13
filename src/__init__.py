from flask import Flask
from src.database import init_db

def create_app(test_config=None):
    app = Flask('FlaskStarter')

    init_db()

    @app.route('/')
    def hello():
        from src.models.user import User
        u = User('hello','world')
        #from src.database import db_session
        #db_session.add(u)
        #db_session.commit()
        return 'Hello World!'
    
    from src.controllers.auth import auth
    app.register_blueprint(auth.bp)


    from src.controllers.account import account
    app.register_blueprint(account.bp)

    return app
