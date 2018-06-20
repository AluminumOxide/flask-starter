from flask import render_template, jsonify, Flask
from src.webexception import WebException
from src.database import Database

def create_app(test_config=None):

    app = Flask('FlaskStarter')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db = Database(app)

    from src.models.user import User
    db.clear()

    @app.route('/')
    def display_index():
        return render_template('index.html')

    @app.errorhandler(WebException)
    def handle_web_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    from src.controllers.auth import auth
    app.register_blueprint(auth.bp)
    
    from src.controllers import account
    app.register_blueprint(account.bp)

    return app
