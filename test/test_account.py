import pytest
from src.webexception import WebException

# check
def test_check_name(app):
    from src.controllers.account import Account
    assert Account().check("name", "testy123")
    assert Account().check("name", "bad!!!!") == 'Name contains non-alphanumeric characters'

def test_check_email():
    from src.controllers.account import Account
    assert Account().check("email", "testy123@test.com")
    assert Account().check("email", "testy123test.com") == 'Email does not contain @'

def test_check_password():
    from src.controllers.account import Account
    assert Account().check("password", "password1234")
    assert Account().check("password", "a") == 'Password length must be at least 6'

def test_check_lang():
    from src.controllers.account import Account
    assert Account().check("lang", "en")
    assert Account().check("lang", "asdf") == 'Language length must be at most 3'

# check_errors
def test_check_errors():
    from src.controllers.account import Account
    e = Account().check_errors({"name":"check!!!", "email":"checktest.com", "password":"d", "lang":"asdf"})
    fields = e.to_dict()['fields']
    assert fields['name'] == 'Name contains non-alphanumeric characters'
    assert fields['email'] == 'Email does not contain @'
    assert fields['password'] == 'Password length must be at least 6'
    assert fields['lang'] == 'Language length must be at most 3'

# create
def test_create():
    from src.controllers.account import Account
    uid = Account().create("create1","create1@test.com","password1","en")
    assert uid is not None

def test_create_error():
    from src.controllers.account import Account
    try:
        uid = Account().create("test&","testtest.com","","asdf")
    except WebException as e:
        fields = e.to_dict()['fields']
        assert fields['name'] == 'Name contains non-alphanumeric characters'
        assert fields['email'] == 'Email does not contain @'
        assert fields['password'] == 'Password length must be at least 6'
        assert fields['lang'] == 'Language length must be at most 3'

# update
def test_update():
    from src.controllers.account import Account
    from src.models.user import User
    uid = Account().update(4, "update1", "update1@test.com", "password123", "fr")
    assert uid is not None
    u = User.query.get(uid)
    assert u.name == "update1"
    assert u.email == "update1@test.com"
    assert u.check_password("password123")
    assert u.lang == "fr"

def test_update_dne():
    from src.controllers.account import Account
    try:
        uid = Account().update(1000, "update1", "update1@test.com", "password123", "fr")
    except WebException as e:
        assert e.to_dict()['message'] == 'User does not exist'

def test_update_error():
    from src.controllers.account import Account
    try:
        uid = Account().update(5, "bad!!!", "badtest.com", "bad", "asdf")
    except WebException as e:
        fields = e.to_dict()['fields']
        assert fields['name'] == 'Name contains non-alphanumeric characters'
        assert fields['email'] == 'Email does not contain @'
        assert fields['password'] == 'Password length must be at least 6'
        assert fields['lang'] == 'Language length must be at most 3'

# delete
def test_delete():
    from src.controllers.account import Account
    from src.models.user import User
    Account().delete(5)
    u = User.query.get(5)
    assert u.deleted

def test_delete_error():
    from src.controllers.account import Account
    try:
        Account().delete(1000)
    except WebException as e:
        assert e.to_dict()['message'] == 'User does not exist'

# purge
def test_purge():
    from src.controllers.account import Account
    from src.models.user import User
    Account().purge(5)
    u = User.query.get(5)
    assert u is None

def test_purge_error():
    from src.controllers.account import Account
    try:
        Account().purge(1000)
    except WebException as e:
        assert e.to_dict()['message'] == 'User does not exist'




