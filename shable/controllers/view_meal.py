from bson import ObjectId
from tg import expose
from shable import model
from shable.lib.base import BaseController

__author__ = 'gas'

class ViewMealController(BaseController):
    @expose('shable.templates.view_meal')
    def index(self, **kw):
        meal = model.Meal.query.get(_id=ObjectId(kw['id']))
        user = model.User.query.get(_id=meal.user_id)
        return {'meal': meal, 'user':user}

    @expose()
    def buy(self, **kw):
        return {}