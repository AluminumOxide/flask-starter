import pytest

def test_test(app, client):
    from src.models.user import User
    u = User.query.filter_by(name='test1').first()
    print(u)
    assert True
