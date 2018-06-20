from flask_sqlalchemy import SQLAlchemy

def get_sqlalchemy():
    return Database.db.db

def get_db():
    return Database.db

class Database():

    # Singletons, yay!
    class __Database:

        def __init__(self, app):
            self.db = SQLAlchemy(app)

        def clear(self):
            self.db.drop_all()
            self.db.create_all()
    
        def add(self, value):
            self.db.session.add(value)
    
        def delete(self, value):
            self.db.session.delete(value)
    
        def commit(self):
            self.db.session.commit()
    
    db = None
    def __init__(self, app):
        if not Database.db:
            Database.db = Database.__Database(app)

    def __getattr__(self, name):
        return getattr(self.db, name)


