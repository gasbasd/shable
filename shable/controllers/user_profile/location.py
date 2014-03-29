from tg import expose
from shable.lib.base import BaseController


class LocationProfileController(BaseController):

    @expose('json')
    def index(self):
        return {}

