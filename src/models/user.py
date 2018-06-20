from src.database import get_sqlalchemy, get_db
from sqlalchemy.orm import validates
from passlib.context import CryptContext
import datetime
import re

db = get_db()
sqla = get_sqlalchemy()
pwd_context = CryptContext(
        schemes=["sha256_crypt","md5_crypt"]
)

class User(sqla.Model):

    __name_len = 50
    __email_len = 120
    __password_len = 120
    __lang_len = 3

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(__name_len), unique=True)
    email = sqla.Column(sqla.String(__email_len), unique=True)
    password = sqla.Column(sqla.String(__password_len))
    lang = sqla.Column(sqla.String(__lang_len))
    created = sqla.Column(sqla.DateTime, default=datetime.datetime.now())
    updated = sqla.Column(sqla.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    deleted = sqla.Column(sqla.Boolean, default=False)
    recovery_field = sqla.Column(sqla.String(50))
    recovery_code = sqla.Column(sqla.String(50))
    verified_email = sqla.Column(sqla.Boolean, default=False)
    verification_code = sqla.Column(sqla.String(50))
    login_code = sqla.Column(sqla.String(50))
    login_timestamp = sqla.Column(sqla.DateTime)

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

    def save(self):
        db.add(self)
        db.commit()

    def check(self, field, value):
        if field == "name":
            try:
                return self.validate_name(field, value) == value
            except:
                return False
        elif field == "email":
            try:
                return self.validate_email(field, value) == value
            except:
                return False
        elif field == "password":
            try:
                return self.validate_password(field, value) == value
            except:
                return False
        elif field == "lang":
            try:
                return self.validate_lang(field, value) == value
            except:
                return False
        return True # TODO: Better validation!

    def update(self, values):
        for key,val in values.items():
            if key == "name":
                self.name = val
            elif key == "email":
                self.email = val
                self.verified_email = False
            elif key == "lang":
                self.lang = val
            elif key == "password":
                self.password = self.encrypt_password(val)
        self.save()

    def delete(self):
        self.deleted = True
        self.save()

    def purge(self):
        db.delete(self)
        db.commit()

    def encrypt_password(self, password):
        return pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

