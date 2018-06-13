from flask import Blueprint, request, render_template

# Routes

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('', methods=['GET','POST','PATCH','DELETE'])
def manage_account():
	"""Endpoint to view/create/update/delete an account"""
	if request.method == 'GET':
		return account_get()
	if request.method == 'POST':
		return account_post()
	if request.method == 'PATCH':
		return account_patch()
	if request.method == 'DELETE':
		return account_delete()

@bp.route('/purge', methods=['GET','DELETE'])
def purge_account():
	"""Endpoint to purge all account data"""
	if request.method == 'GET':
		return purge_account_get()
	if request.method == 'DELETE':
		return purge_account_delete()

@bp.route('/verify/email', methods=['GET','POST'])
def verify_email():
	"""Endpoint to verify email address"""
	if request.method == 'GET':
		return verify_email_get()
	if request.method == 'POST':
		return verify_email_post()

@bp.route('/recover/password', methods=['GET','POST'])
def recover_password():
	"""Endpoint to recover password"""
	if request.method == 'GET':
		return recover_password_get()
	if request.method == 'POST':
		return recover_password_post()

@bp.route('/recover/deleted', methods=['GET','POST'])
def recover_deleted():
	"""Endpoint to recover a deleted account"""
	if request.method == 'GET':
		return recover_deleted_get()
	if request.method == 'POST':
		return recover_deleted_post()

@bp.route('/recover/name', methods=['GET','POST'])
def recover_name():
	"""Endpoint to recover username"""
	if request.method == 'GET':
		return recover_name_get()
	if request.method == 'POST':
		return recover_name_post()

@bp.route('/check/name', methods=['POST'])
def check_name():
	"""Endpoint to check if a username would be valid"""
	return check_name_post()

@bp.route('/check/email', methods=['POST'])
def check_email():
	"""Endpoint to check if an email would be valid"""
	return check_email_post()

@bp.route('/check/password', methods=['POST'])
def check_password():
	"""Endpoint to check if a passwould would be valid"""
	return check_password_post()

@bp.route('/check/language', methods=['POST'])
def check_language():
	"""Endpoint to check if a default language is supported"""
	return check_language_post()

# Controllers

def account_get():
	"""Displays account information"""
	return render_template('account/account.html')

def account_post():
	"""Creates an account"""
	return "CREATE"

def account_patch():
	"""Updates an account"""
	return "UPDATE"

def account_delete():
	"""Deletes an account"""
	return "DELETE"

def purge_account_get():
	"""Displays form to purge account"""
	return render_template('account/purge_account.html')

def purge_account_delete():
	"""Purges an account and account data"""
	return "PURGE"

def verify_email_get():
	"""Displays email verification form"""
	return render_template('account/verify_email.html')

def verify_email_post():
	"""Verifies an email"""
	return "VERIFY EMAIL"

def recover_password_get():
	"""Displays password recovery form"""
	return render_template('account/recover_password.html')

def recover_password_post():
	"""Recovers a password"""
	return "RECOVER PASSWORD"

def recover_deleted_get():
	"""Displays a form to recover a deleted account"""
	return render_template('account/recover_deleted.html')

def recover_deleted_post():
	"""Recovers a deleted account"""
	return "RECOVER DELETED"

def recover_name_get():
	"""Displays a form to recover a username"""
	return render_template('account/recover_name.html')

def recover_name_post():
	"""Recovers a username"""
	return "RECOVER USERNAME"

def check_name_post():
	"""Checks if a username would be valid"""
	return "CHECK USERNAME"

def check_email_post():
	"""Checks if an email would be valid"""
	return "CHECK EMAIL"

def check_password_post():
	"""Checks if a password would be valid"""
	return "CHECK PASSWORD"

def check_language_post():
	"""Checks if a default language is supported"""
	return "CHECK LANG"
