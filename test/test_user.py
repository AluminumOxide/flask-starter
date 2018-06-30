import pytest

def test_test():
    from src.models.user import User
    assert True

# check
def test_check_name():
    from src.models.user import User
    u = User()
    assert u.check("name", "testy123")
    assert u.check("name", "t")
    assert u.check("name", "12345678901234567890123456789012345678901234567890")
    assert u.check("name", "test1") == "Name is not unique"
    assert u.check("name", "") == "Name length must be at least 1"
    assert u.check("name", "123456789012345678901234567890123456789012345678901") == "Name length must be at most 50"
    assert u.check("name", "!@#$%^&*().,><?/{}[]") == "Name contains non-alphanumeric characters"

def test_check_email():
    from src.models.user import User
    u = User()
    assert u.check("email", "testy123@test.com")
    assert u.check("email", "test1@test.com") == "Email is not unique"
    assert u.check("email", "testy123test.com") == "Email does not contain @"
    assert u.check("email", "testy123@testcom") == "Email does not contain ."
    assert u.check("email", "@.") == "Email length must be at least 5"
    assert u.check("email", "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901@test.com") == "Email length must be at most 120"

def test_check_password():
    from src.models.user import User
    u = User()
    assert u.check("password", "password123")
    assert u.check("password", "asdf") == "Password length must be at least 6"
    assert u.check("password","1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901") == "Password length must be at most 120"

def test_check_lang():
    from src.models.user import User
    u = User()
    assert u.check("lang", "en")
    assert u.check("lang", "fr")
    assert u.check("lang", "") == "Language length must be at least 1"
    assert u.check("lang", "asdf") == "Language length must be at most 3"

# save
def test_save():
    from src.models.user import User
    u = User.query.filter_by(name='test1').first()
    u.lang = 'fr'
    u.save()
    v = User.query.filter_by(name='test1').first()
    assert v.lang == 'fr'

# init
def test_init():
    from src.models.user import User
    u = User('testy','testy@test.com','password','en')
    assert u.name is 'testy'
    assert u.email is 'testy@test.com'
    assert u.password is not None
    assert u.password is not 'password'
    assert u.check_password('password')
    assert u.lang is 'en'
    assert not u.verified_email
    assert len(u.verification_code) == 50

def test_init_noargs():
    from src.models.user import User
    u = User()
    assert u.name is None
    assert u.email is None
    assert u.password is None
    assert u.lang is None

# update
def test_update():
    from src.models.user import User
    u = User.query.filter_by(name='test3').first()
    u.update({'name':'test33', 'email':'test33@test.com', 'password':'password33', 'lang':'fr'})
    v = User.query.filter_by(name='test3').first()
    assert v is None
    v = User.query.filter_by(name='test33').first()
    assert v.name == 'test33'
    assert v.email == 'test33@test.com'
    assert v.check_password('password33')
    assert v.lang == 'fr'

# delete
def test_delete():
    from src.models.user import User
    u = User.query.filter_by(name='test1').first()
    u.delete()
    v = User.query.filter_by(name='test1').first()
    assert v.deleted == True
    
# purge
def test_purge():
    from src.models.user import User
    u = User.query.filter_by(name='test2').first()
    u.purge()
    v = User.query.filter_by(name='test2').first()
    assert v is None

# verify email
def verify_email():
    u = User.query.filter_by(name='testy').first()
    assert u.verify_email(u.verification_code)
    assert u.verified_email
    assert len(u.verification_code) == 0

def verify_email_error():
    u = User.query.filter_by(name='test1').first()
    assert not u.verify_email("BADCODE!")
    assert not u.verified_email



