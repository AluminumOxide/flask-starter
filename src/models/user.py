from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
#    password_salt = Column(String())
#    password_encrypted = Column(String())
#    lang = Column(String())
#    created = Column()
#    updated = Column()
#    deleted = Column(Boolean)
#    recovery_field = Column()
#    recovery_code = Column()
#    verified_email = Column()
#    verification_code = Column()
#    login_code = Column()
#    login_timestamp = Column()
    

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.id)


