from src import db

class User(db.Model):

    print("USER LOADED")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_salt = db.Column(db.String(10))
    password_encrypted = db.Column(db.String(120))
    lang = db.Column(db.String(3))
##    created = db.Column()
##    updated = db.Column()
##    deleted = db.Column(Boolean)
##    recovery_field = db.Column()
##    recovery_code = db.Column()
##    verified_email = db.Column()
##    verification_code = db.Column()
##    login_code = db.Column()
##    login_timestamp = db.Column()
    

    def __init__(self, name=None, email=None, password=None, lang=None):
        self.name = name
        self.email = email
        self.password_salt = ""
        self.password_encrypted = ""
        self.lang = lang

    def __repr__(self):
        return '<User %r>' % (self.id)


