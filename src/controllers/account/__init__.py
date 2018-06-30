from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from .account import Account
from src.models.user import User
from src.webexception import WebException

# Routes

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/', methods=['GET','POST'])
def create_account():
    """Endpoint to create an account"""
    if request.method == 'GET':
        return create_account_get()
    if request.method == 'POST':
        return create_account_post()

@bp.route('/<int:user_id>', methods=['GET','POST'])
def manage_account(user_id):
    """Endpoint to view and update an account"""
    if request.method == 'GET':
        return account_get(user_id)
    if request.method == 'POST':
        return account_post(user_id)

@bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_account(user_id):
    """Endpoint to delete an account"""
    if request.method == 'POST':
        return delete_account_post(user_id)

@bp.route('/<int:user_id>/purge', methods=['POST'])
def purge_account(user_id):
    """Endpoint to purge all account data"""
    if request.method == 'POST':
        return purge_account_post(user_id)

@bp.route('/<int:user_id>/verify/email', methods=['GET','POST'])
def verify_email(user_id):
    """Endpoint to verify email address"""
    if request.method == 'GET':
        return verify_email_get(user_id)
    if request.method == 'POST':
        return verify_email_post(user_id)

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

def account_get(user_id, error=None):
    """Displays account information"""
    u = User.query.get(user_id)
    if not u:
        raise WebException('User does not exist')
    elif u.deleted:
        return recover_deleted_get()
    elif u.verified_email:
        return render_template('account/account.html', user=User.query.get(user_id), error=error)
    else:
        return verify_email_get(user_id)

def account_post(user_id):
    """Updates an account"""
    try:
        Account().update(
                user_id, 
                request.form.get('name'), 
                request.form.get('email'), 
                request.form.get('password'), 
                request.form.get('lang'))
        return redirect(url_for('account.manage_account', user_id=user_id))
    except WebException as e:
        return account_get(e.to_dict())

def create_account_get(error=None):
    """Displays form to create account"""
    return render_template('account/create.html',error=error)

def create_account_post():
    """Creates a new account"""
    try:
        user_id = Account().create(
                request.form.get('name'), 
                request.form.get('email'), 
                request.form.get('password'), 
                request.form.get('lang'))
        return redirect(url_for('account.manage_account', user_id=user_id))
    except WebException as e:
        return create_account_get(e.to_dict())

def delete_account_post(user_id):
    """Marks an account as deleted"""
    Account().delete(user_id)
    return render_template('account/delete.html')

def purge_account_post(user_id):
    """Purges an account and account data"""
    Account().purge(user_id)
    return render_template('account/purge.html')

def check_name_post():
    """Checks if a username would be valid"""
    return jsonify(Account().check("name", request.form.get('name')))

def check_email_post():
    """Checks if an email would be valid"""
    return jsonify(Account().check("email", request.form.get('email')))

def check_password_post():
    """Checks if a password would be valid"""
    return jsonify(Account().check("password", request.form.get('password')))

def check_language_post():
    """Checks if a default language is supported"""
    return jsonify(Account().check("lang", request.form.get('lang')))

def verify_email_get(user_id, error=None):
    """Displays email verification form"""
    return render_template('account/verify_email.html', user_id=user_id)

def verify_email_post(user_id):
    """Verifies an email"""
    resend = request.form.get('resend')
    if resend == "True":
        u = User.query.get(user_id)
        print("SEND EMAIL TO %s VERIFICATION CODE %s" % (u.id, u.verification_code))
    if Account().verify_email(user_id, request.form.get('code')):
        return account_get(user_id)
    return verify_email_get(user_id, 'Invalid email verification code')





def recover_password_get():
    """Displays password recovery form"""
    return render_template('account/recover_password.html')

def recover_password_post():
    """Recovers a password"""
    return Account().recover("password")

def recover_deleted_get():
    """Displays a form to recover a deleted account"""
    return render_template('account/recover_deleted.html')

def recover_deleted_post():
    """Recovers a deleted account"""
    return Account().recover("deleted")

def recover_name_get():
    """Displays a form to recover a username"""
    return render_template('account/recover_name.html')

def recover_name_post():
    """Recovers a username"""
    return Account().recover("name")


