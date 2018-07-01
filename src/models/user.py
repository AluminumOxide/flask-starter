from src.database import get_sqlalchemy, get_db
from sqlalchemy.orm import validates
from passlib.context import CryptContext
import datetime
import random, string
import re
from flask_babel import _

db = get_db()
sqla = get_sqlalchemy()
pwd_context = CryptContext(
        schemes=["sha256_crypt","md5_crypt"]
)

class User(sqla.Model):

    __name_len_max = 50
    __name_len_min = 1
    __email_len_max = 120
    __email_len_min = 5
    __password_len_max = 120
    __password_len_min = 6
    __lang_len_max = 3
    __lang_len_min = 1
    __vericode_len = 50

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String(__name_len_max), unique=True)
    email = sqla.Column(sqla.String(__email_len_max), unique=True)
    password = sqla.Column(sqla.String(__password_len_max))
    lang = sqla.Column(sqla.String(__lang_len_max))
    created = sqla.Column(sqla.DateTime, default=datetime.datetime.now())
    updated = sqla.Column(sqla.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    deleted = sqla.Column(sqla.Boolean, default=False)
    recovery_field = sqla.Column(sqla.String(50))
    recovery_code = sqla.Column(sqla.String(50))
    verified_email = sqla.Column(sqla.Boolean, default=False)
    verification_code = sqla.Column(sqla.String(__vericode_len))
    login_code = sqla.Column(sqla.String(50))
    login_timestamp = sqla.Column(sqla.DateTime)

    @validates('name')
    def validate_name(self, key, name):
        assert len(name) >= self.__name_len_min, _("error.user-name-min-len", l=self.__name_len_min)
        assert len(name) <= self.__name_len_max, _("error.user-name-max-len", l=self.__name_len_max)
        assert re.match('^[^\W_]+$', name), _("error.user-name-alphanumeric")
        u = self.query.filter_by(name=name).first()
        assert u is None, _("error.user-name-not-unique")
        return name

    @validates('email')
    def validate_email(self, key, email):
        assert len(email) >= self.__email_len_min, _("error.user-email-min-len", l=self.__email_len_min)
        assert len(email) <= self.__email_len_max, _("error.user-email-max-len", l=self.__email_len_max)
        assert '@' in email, _("error.user-email-missing-at")
        assert '.' in email, _("error.user-email-missing-period")
        u = self.query.filter_by(email=email).first()
        assert u is None, _("error.user-email-not-unique")
        return email

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >= self.__password_len_min, _("error.user-password-min-len", l=self.__password_len_min)
        assert len(password) <= self.__password_len_max, _("error.user-password-max-len", l=self.__password_len_max)
        return password

    @validates('lang')
    def validate_lang(self, key, lang):
        #TODO: Check i18n
        assert len(lang) >= self.__lang_len_min, _("error.user-lang-min-len", l=self.__lang_len_min)
        assert len(lang) <= self.__lang_len_max, _("error.user-lang-max-len", l=self.__lang_len_max)
        return lang

    def __init__(self, name=None, email=None, password=None, lang=None):
        if name:
            self.name = name
        if email:
            self.email = email
            self.verified_email = False
            self.verification_code = ''.join(random.choices(string.ascii_uppercase, k=50))
            print("SEND EMAIL FOR USERID %s WITH VERIFICATION %s" % (self.id, self.verification_code)) #TODO!
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
            except AssertionError as e:
                return str(e)
            except:
                return False
        elif field == "email":
            try:
                return self.validate_email(field, value) == value
            except AssertionError as e:
                return str(e)
            except:
                return False
        elif field == "password":
            try:
                return self.validate_password(field, value) == value
            except AssertionError as e:
                return str(e)
            except:
                return False
        elif field == "lang":
            try:
                return self.validate_lang(field, value) == value
            except AssertionError as e:
                return str(e)
            except:
                return False
        return True

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

    def verify_email(self, code):
        if code == self.verification_code:
            self.verified_email = True
            self.verification_code = ""
            self.save()
            return True
        else:
            return False
