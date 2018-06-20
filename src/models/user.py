from src import db
from passlib.context import CryptContext
import datetime
from sqlalchemy.orm import validates
import re

pwd_context = CryptContext(
        schemes=["sha256_crypt","md5_crypt"]
)

class User(db.Model):

    __name_len = 50
    __email_len = 120
    __password_len = 120
    __lang_len = 3

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(__name_len), unique=True)
    email = db.Column(db.String(__email_len), unique=True)
    password = db.Column(db.String(__password_len))
    lang = db.Column(db.String(__lang_len))
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    updated = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    deleted = db.Column(db.Boolean, default=False)
    recovery_field = db.Column(db.String(50))
    recovery_code = db.Column(db.String(50))
    verified_email = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(50))
    login_code = db.Column(db.String(50))
    login_timestamp = db.Column(db.DateTime)

    @validates('name')
    def validate_name(self, key, name):
        u = self.query.filter_by(name=name).first()
        assert u is None
        assert re.match('^[^\W_]+$', name)
        assert len(name) >= 1
        assert len(name) <= self.__name_len
        return name

    @validates('email')
    def validate_email(self, key, email):
        u = self.query.filter_by(email=email).first()
        assert u is None
        assert '@' in email
        assert len(email) <= self.__email_len
        return email

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) <= self.__password_len
        return password

    @validates('lang')
    def validate_lang(self, key, lang):
        #TODO: Check i18n
        assert len(lang) <= self.__lang_len
        return lang

    def __init__(self, name=None, email=None, password=None, lang=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = self.encrypt_password(password)
        if lang:
            self.lang = lang

    def __repr__(self):
        return '<User %r>' % (self.id)

    def encrypt_password(self, password):
        return pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

