from src.models.user import User
from src.webexception import WebException

class Account:

    def create(self, name, email, password, lang):
        """Creates a new user account"""
        error = self.check_errors({'name':name,'email':email,'password':password,'lang':lang})
        if error is not None:
            raise error
        u = User(name, email, password, lang)
        u.save()
        return u.id

    def update(self, user_id, name, email, password, lang):
        """Updates a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        changes = {}
        if name and u.name != name:
            changes['name'] = name
        if email and u.email != email:
            changes['email'] = email
        if lang and u.lang != lang:
            changes['lang'] = lang
        if password and not u.check_password(password):
            changes['password'] = password
        error = self.check_errors(changes)
        if error is not None:
            raise error
        u.update(changes)
        return u.id

    def delete(self, user_id):
        """Deletes a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        u.delete()
        return 

    def purge(self, user_id):
        """Purges a user account"""
        u = User.query.get(user_id)
        if not u:
            raise WebException('User does not exist')
        u.purge()
        return 

    def check(self, field, value):
        """Checks if a field value would be valid"""
        return User().check(field, value)

    def check_errors(self, values):
        """Checks multiple values and constructs an exception if necessary"""
        error = { 'fields':{}, 'context':values } #TODO: store error messages w/ fields
        for field in values:
            c = self.check(field, values[field])
            if not c == True:
                error['fields'][field] = c
                #error['fields'].append(field)
        if not error['fields']:
            return None
        return WebException('Invalid value(s)', None, error)

    def recover(self, field):
        """Recovers a user account"""
        return "RECOVER"+field

    def verify(self, field, value):
        """Verifies a field"""
        return "VERIFY"+field
