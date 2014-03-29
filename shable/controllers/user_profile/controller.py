from tg import predicates, expose
from shable.lib.base import BaseController


class UserProfileController(BaseController):
    allow_only = predicates.not_anonymous()

    @expose('json')
    def index(self):
        return {'hello': 'world'}
