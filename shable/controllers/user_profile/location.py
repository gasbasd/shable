# coding=utf-8
from __future__ import unicode_literals
from tg import expose, lurl, predicates, redirect, flash, request
from tw2.forms import ListForm, TextField, SingleSelectField, SubmitButton, TextArea, CheckBoxList
from shable.lib.base import BaseController
from shable.model.models import FOOD_TYPES, LOCATION_PREFERENCES


class LocationProfileForm(ListForm):
    css_class = 'shable-form'
    description = TextArea(label='Descrizione breve', css_class='form-control')
    #details = TextArea(label='Dettagli su non so cosa', css_class='form-control')
    address = TextField(label='Indirizzo', css_class='form-control')
    number = TextField(label='Numero', css_class='form-control')
    city = TextField(label='Città', css_class='form-control')
    zip_code = TextField(label='CAP', css_class='form-control')
    food_types = CheckBoxList(label='Preferenze cibi', css_class='form-control',  options = FOOD_TYPES)
    preferences = CheckBoxList(label='Preferenze alimentazione', css_class='form-control',  options = LOCATION_PREFERENCES)
    #add a photo

    submit = SubmitButton(value='Salva Location', css_class='form-control')
    action = lurl('/user_profile/location/update_details')


class LocationProfileController(BaseController):
    allow_only = predicates.not_anonymous()

    @expose('shable.templates.user_profile.location')
    def index(self):
        user = request.identity['user']
        return {'form': LocationProfileForm, 'value': user.location}

    @expose()
    def update_details(self, **kw):
        user = request.identity['user']
        user.location.description = kw['description']
        user.location.address = kw['address']
        user.location.number = kw['number']
        user.location.city = kw['city']
        user.location.zip_code = kw['zip_code']

        if kw.get('food_types') is not None:
            if not isinstance(kw.get('food_types'),list):
                user.location.food_types = [kw.get('food_types')]
            else:
                user.location.food_types = kw.get('food_types')
        else:
            user.location.food_types = []

        if kw.get('preferences') is not None:
            if not isinstance(kw.get('preferences'),list):
                user.location.preferences = [kw.get('preferences')]
            else:
                user.location.preferences = kw.get('preferences')
        else:
            user.location.preferences = []

        flash('Tavolalvata')
        redirect('/user_profile/location')

