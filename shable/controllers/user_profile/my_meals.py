# coding=utf-8
from __future__ import unicode_literals
from bson import ObjectId

from tg import request, expose, redirect, lurl
from tw2.forms import HiddenField, SingleSelectField, SubmitButton, ListForm, TextArea
from shable import model
from shable.lib.base import BaseController


class MealFeedBackForm(ListForm):
    css_class = 'shable-form'
    meal_id = HiddenField()
    comment = TextArea(label='COMMENTO', css_class='form-control')
    cleaning = SingleSelectField(label='Pulizia', css_class='form-control small-single-select', options=[i for i in range(6)])
    food_quality = SingleSelectField(label='Qualità', css_class='form-control small-single-select', options=[i for i in range(6)])
    cordiality = SingleSelectField(label='Cordialità', css_class='form-control small-single-select', options=[i for i in range(6)])
    punctuality = SingleSelectField(label='Puntualità', css_class='form-control small-single-select', options=[i for i in range(6)])
    sociality = SingleSelectField(label='Socialità', css_class='form-control small-single-select', options=[i for i in range(6)])
    submit = SubmitButton(value='LASCIA FEEDBACK', css_class='form-control')
    action = lurl('/user_profile/past_meals/save_feedback')

class PastMealsController(BaseController):

    @expose('shable.templates.user_profile.my_meal')
    def index(self):
        user = request.identity['user']
        if getattr(user, 'my_meals', False):
            meals = model.Meal.query.find({'_id': {'$in': user.my_meals}})
        else:
            meals = []
        return {'meals': meals}

    @expose('shable.templates.user_profile.leave_feedback')
    def leave_feedback(self, **kw):
        return {'form': MealFeedBackForm, 'value': {'meal_id': kw['meal_id']}}

    @expose()
    def save_feedback(self, **kw):
        meal = model.Meal.query.get(_id=ObjectId(kw.pop('meal_id')))
        user = model.User.query.get(_id=meal.user_id)
        buyer = request.identity['user']
        feed = {'user': buyer.display_name, 'comment': kw.pop('comment'), 'rates': [{k: v} for k, v in kw.iteritems()]}
        user.location.feedback.append(feed)
        redirect('/user_profile/past_meals')

