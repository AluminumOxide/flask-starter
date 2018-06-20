from src.models.user import User
from src import db
from src.webexception import WebException

class Account:

    def create(self, name, email, password, lang):
        """Creates a new user account"""
        error = self.check_errors({'name':name,'email':email,'password':password,'lang':lang})
        if error is not None:
            raise error
        u = User(name, email, password, lang)
        db.session.add(u)
        db.session.commit()
        return u.id

    def update(self, user_id, name, email, password, lang):
        """Updates a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        context = {}
        if name and u.name != name:
            context['name'] = name
            u.name = name
        if email and u.email != email:
            context['email'] = email
            u.email = email
            u.verified_email = False
        if lang and u.lang != lang:
            context['lang'] = lang
            u.lang = lang
        if password and not u.check_password(password):
            context['password'] = password
            u.password = u.encrypt_password(password)
        error = self.check_errors(context)
        if error is not None:
            raise error
        db.session.add(u)
        db.session.commit()
        return u.id

    def delete(self, user_id):
        """Deletes a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        u.deleted = True
        db.session.add(u)
        db.session.commit()
        return 

    def purge(self, user_id):
        """Purges a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        db.session.delete(u)
        db.session.commit()
        return 

    def check_errors(self, context):
        """Checks multiple values and constructs an exception if necessary"""
        error = { 'fields':[], 'context':context }
        for field in context:
            if not self.check(field, context[field]):
                error['fields'].append(field)
        if len(error['fields']) == 0:
            return None
        return WebException('Invalid value(s)', None, error)

    def check(self, field, value):
        """Checks if a field value would be valid"""
        u = User()
        if field == "name":
            print("CHECK NAME")
            try:
                return u.validate_name(field, value) == value
            except:
                return False
        elif field == "email":
            try:
                return u.validate_email(field, value) == value
            except:
                return False
        elif field == "password":
            try:
                return u.validate_password(field, value) == value
            except:
                return False
        elif field == "lang":
            try:
                return u.validate_lang(field, value) == value
            except:
                return False
        return True

    def recover(self, field):
        """Recovers a user account"""
        return "RECOVER"+field

    def verify(self, field, value):
        """Verifies a field"""
        return "VERIFY"+field
