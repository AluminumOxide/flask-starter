from src.models.user import User
from src import db

class Account:

    def create(name, email, password, lang):
        """Creates a new user account"""
        u = User(name, email, password, lang)
        db.session.add(u)
        db.session.commit()
        return "CREATE"

    def update():
        """Updates a user account"""
        return "UPDATE"

    def delete():
        """Deletes a user account"""
        return "DELETE"

    def purge():
        """Purges a user account"""
        return "PURGE"

    def recover(field):
        """Recovers a user account"""
        return "RECOVER"+field

    def check(field, value):
        """Checks if a field value would be valid"""
        return "CHECK"+field

    def verify(field, value):
        """Verifis a field"""
        return "VERIFY"+field
