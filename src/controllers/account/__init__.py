from flask import Blueprint, request, render_template
from .account import Account

# Routes

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('', methods=['GET','POST','DELETE'])
def manage_account():
    """Endpoint to view/create/update/delete an account"""
    if request.method == 'GET':
        return account_get()
    if request.method == 'POST':
        return account_post()
    if request.method == 'DELETE':
        return account_delete()

@bp.route('/create', methods=['GET','POST'])
def create_account():
    if request.method == 'GET':
        return create_account_get()
    if request.method == 'POST':

        return create_account_post()

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
    """Updates an account"""
    return Account.update()

def account_delete():
    """Deletes an account"""
    return Account.delete()

def create_account_get():
    """Displays from to create account"""
    return render_template('account/create.html')

def create_account_post():
    """Creates a new account"""
    return Account.create(request.form.get('name'), request.form.get('email'), request.form.get('password'), request.form.get('lang'))

def purge_account_get():
    """Displays form to purge account"""
    return render_template('account/purge.html')

def purge_account_delete():
    """Purges an account and account data"""
    return Account.purge()

def verify_email_get():
    """Displays email verification form"""
    return render_template('account/verify_email.html')

def verify_email_post():
    """Verifies an email"""
    return Account.verify("email","")

def recover_password_get():
    """Displays password recovery form"""
    return render_template('account/recover_password.html')

def recover_password_post():
    """Recovers a password"""
    return Account.recover("password")

def recover_deleted_get():
    """Displays a form to recover a deleted account"""
    return render_template('account/recover_deleted.html')

def recover_deleted_post():
    """Recovers a deleted account"""
    return Account.recover("deleted")

def recover_name_get():
    """Displays a form to recover a username"""
    return render_template('account/recover_name.html')

def recover_name_post():
    """Recovers a username"""
    return Account.recover("name")

def check_name_post():
    """Checks if a username would be valid"""
    return Account.check("name","")

def check_email_post():
    """Checks if an email would be valid"""
    return Account.check("email","")

def check_password_post():
    """Checks if a password would be valid"""
    return Account.check("password","")

def check_language_post():
    """Checks if a default language is supported"""
    return Account.check("lang","")
