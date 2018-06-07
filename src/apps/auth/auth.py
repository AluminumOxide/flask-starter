from flask import Blueprint, render_template, request

# Routes

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET','POST'])
def login():
	"""Endpoint to login"""
	if request.method == 'GET':
		return login_get()
	if request.method == 'POST':
		return login_post()

@bp.route('/logout', methods=['GET','POST'])
def logout():
	"""Endpoint to logout"""
	if request.method == 'GET':
		return logout_get()
	if request.method == 'POST':
		return logout_post()

# Controllers

def login_get():
	"""Displays a login form"""
	return render_template('auth/login.html')

def login_post():
	"""Logs a user in"""
	return "LOGIN"

def logout_get():
	"""Displays a logout page"""
	return render_template('auth/logout.html')

def logout_post():
	"""Logs a user out"""
	return "LOGOUT"
