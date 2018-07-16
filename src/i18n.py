from flask import request
from flask_babel import Babel

def list_locales():
    return I18n.i18n.list_locales()

def list_locale():
    return request.accept_languages.best_match(I18n.i18n.list_locales())



class I18n():

    class __I18n:

        def __init__(self, app):
            self.i18n = Babel(app)
            self.localeselector = self.i18n.localeselector

        def list_locales(self):
            return list(map(lambda t: str(t), self.i18n.list_translations()))

    i18n = None
    def __init__(self, app=None):

        if not I18n.i18n and app:
            I18n.i18n = I18n.__I18n(app)

            @I18n.i18n.localeselector
            def get_locale():
                return request.accept_languages.best_match(I18n.i18n.list_locales())

    def __getattr__(self, name):
        return getattr(self.i18n, name)


