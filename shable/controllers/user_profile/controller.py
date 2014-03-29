from tg import predicates, expose, lurl
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
    @expose('json')
    def index(self):
        return {'hello': 'world'}

    def update_profile(self):
        return {}
