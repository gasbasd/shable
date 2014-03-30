from bson import ObjectId
from tg import expose, lurl, request, flash, redirect
from tw2.forms import ListForm, SingleSelectField, HiddenField, SubmitButton
from shable import model
from shable.lib.base import BaseController

class BuyMealForm(ListForm):
    css_class = 'shable-form'
    meal_id = HiddenField()
    quantity = SingleSelectField(label=None, css_class='form-control small-single-select', options=[])
    submit = SubmitButton(value='ACQUISTA', css_class='form-control')
    action = lurl('/view_meal/buy')

    def prepare(self):
        id = request.params.getone('id')
        meal = model.Meal.query.get(_id=ObjectId(id))
        for k in self.child.children:
            if k.key == 'quantity':
                k.options = [i for i in range(meal.availability)]
        super(BuyMealForm, self).prepare()


class ViewMealController(BaseController):
    @expose('shable.templates.view_meal')
    def index(self, **kw):
        meal = model.Meal.query.get(_id=ObjectId(kw['id']))
        user = model.User.query.get(_id=meal.user_id)
        return {'meal': meal, 'user': user, 'form': BuyMealForm, 'value': {'meal_id': str(meal._id)}}

    @expose()
    def buy(self, **kw):
        meal = model.Meal.query.get(_id=ObjectId(kw['meal_id']))
        meal.availability -= int(kw['quantity'])
        user = model.User.query.get(_id=meal.user_id)
        user.my_meals.append(meal._id)
        flash('Pasto acquistato!')
        redirect('/view_meal', params={'id':kw['meal_id']})