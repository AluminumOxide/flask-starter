import pytest

def test_test(app, client):
    from src.models.user import User
    assert True

# check
def test_check_name():
    from src.models.user import User
    u = User()
    assert u.check("name", "testy123")
    assert u.check("name", "t")
    assert u.check("name", "12345678901234567890123456789012345678901234567890")
    assert not u.check("name", "test1")
    assert not u.check("name", "")
    assert not u.check("name", "123456789012345678901234567890123456789012345678901")
    assert not u.check("name", "!@#$%^&*().,><?/{}[]")

def test_check_email():
    from src.models.user import User
    u = User()
    assert u.check("email", "testy123@test.com")
    assert not u.check("email", "test1@test")
    assert not u.check("email", "testy123test.com")
    assert not u.check("email", "testy123@testcom")
    assert not u.check("email", "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901@test.com")

def test_check_password():
    from src.models.user import User
    u = User()
    assert u.check("password", "password123")
    assert not u.check("password","1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901") 

def test_check_lang():
    from src.models.user import User
    u = User()
    assert u.check("lang", "en")
    assert u.check("lang", "fr")
    assert not u.check("lang", "asdf")

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
    u.update({'name':'test4', 'email':'test4@test.com', 'password':'password4', 'lang':'fr'})
    v = User.query.filter_by(name='test3').first()
    assert v is None
    v = User.query.filter_by(name='test4').first()
    assert v.name == 'test4'
    assert v.email == 'test4@test.com'
    assert v.check_password('password4')
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

