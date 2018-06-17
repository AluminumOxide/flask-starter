from flask_sqlalchemy import SQLAlchemy

class Database():

    def __init__(self, app):

        # Set test DB URI
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

        # Initialize SQLiteDB
        self.db = SQLAlchemy(app)

        # Set up operation to clear test data and reset tables
        def _clear():
            self.db.drop_all()
            self.db.create_all()
        self.db.clear = _clear

