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

        def import_models(self):
            from src.models.user import User

        def create(self):
            self.db.create_all()

        def clear(self):
            self.db.drop_all()

        def add(self, value):
            self.db.session.add(value)
    
        def delete(self, value):
            self.db.session.delete(value)
    
        def commit(self):
            self.db.session.commit()

        def run_sql(self, sql_array):
            for sql in sql_array:
                self.db.session.execute(sql)
            self.commit()

    db = None
    def __init__(self, app=None):
        if not Database.db and app:
            Database.db = Database.__Database(app)
            Database.db.import_models()
            app_env = app.config['environment']
            if app_env == "test" or app_env == "dev":
                Database.db.clear()
            Database.db.create()

    def __getattr__(self, name):
        return getattr(self.db, name)


