# coding=utf-8
from __future__ import unicode_literals

from tg import predicates, expose, lurl, redirect, request, flash
from tw2.forms import TableForm, ListForm, TextField, SingleSelectField, SubmitButton
from shable.controllers.user_profile.location import LocationProfileController
from shable.lib.base import BaseController


class UserProfileForm(ListForm):
    css_class = 'shable-form'
    name = TextField(label='NOME', css_class='form-control')
    surname = TextField(label='COGNOME', css_class='form-control')
    gender = SingleSelectField(label='SESSO', css_class='form-control', options=['M', 'F'])
    submit = SubmitButton(value='Salva Profilo', css_class='form-control')
    action = lurl('/user_profile/update_profile')


class UserProfileController(BaseController):
    allow_only = predicates.not_anonymous()

    location = LocationProfileController()
    @expose('shable.templates.user_profile.index')
    def index(self):
        user = request.identity['user']
        return {'form': UserProfileForm, 'value': user}

    @expose()
    def update_profile(self, **kw):
        user = request.identity['user']
        user.name = kw['name']
        user.surname = kw['surname']
        user.gender = kw['gender']
        flash('Profilo aggiornato!')
        redirect('/user_profile')
