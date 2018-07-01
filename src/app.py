from flask import render_template, jsonify, Flask, request
from flask_babel import Babel
from src.webexception import WebException
from src.database import Database
from src.config import Config

def create_app(env):

    app = Flask('FlaskStarter')
    
    if env == "test":
        app.config.update(Config[env])
    else:
        app.config.update(Config["dev"])

    babel = Babel(app)

    db = Database(app)

    @app.route('/')
    def display_index():
        return render_template('index.html')

    @app.errorhandler(WebException)
    def handle_web_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(list(map(lambda b: str(b), babel.list_translations())))

    from src.controllers.auth import auth
    app.register_blueprint(auth.bp)
    
    from src.controllers import account
    app.register_blueprint(account.bp)

    return app


