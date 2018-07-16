from flask import render_template, jsonify, Flask, request
from src.webexception import WebException
from src.database import Database
from src.i18n import I18n, list_locales, list_locale
from src.config import Config

def create_app(env):

    # Set up the app
    app = Flask('FlaskStarter')
    app.config.update(Config["all"])
    if env == "test":
        app.config.update(Config[env])
    else:
        app.config.update(Config["dev"])

    # Set up DB
    db = Database(app)

    # Set up i18n
    i18n = I18n(app)

    # Set current locale for jinja access
    @app.before_request
    def before_request():
        app.jinja_env.globals['current_locale'] = list_locale()

    # Add index route
    @app.route('/')
    def display_index():
        return render_template('index.html')

    # List supported languages
    @app.route('/i18n', methods=['GET'])
    def get_i18n():
        if request.method == 'GET':
            return jsonify(list_locales())

    # Handle exceptions
    @app.errorhandler(WebException)
    def handle_web_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Import controllers
    from src.controllers.auth import auth
    app.register_blueprint(auth.bp)
    
    from src.controllers import account
    app.register_blueprint(account.bp)

    return app


