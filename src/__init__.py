from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__)
	
	@app.route('/')
	def hello():
		return 'Hello World!'
	
	from src.apps.auth import auth
	app.register_blueprint(auth.bp)


	from src.apps.account import account
	app.register_blueprint(account.bp)

	return app
