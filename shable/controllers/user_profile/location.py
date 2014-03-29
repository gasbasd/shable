# coding=utf-8
from __future__ import unicode_literals
from axf.widgets.ajax_manage_photos import AjaxManagePhotos
from tg import expose, lurl, predicates, redirect, flash, request
from tw2.forms import ListForm, TextField, SingleSelectField, SubmitButton, TextArea, CheckBoxList
from shable.controllers.utils.temporary_photos import TemporaryPhotosUploader
from shable.lib.base import BaseController
from shable.lib.utils import json_lurl
from shable.model.models import FOOD_TYPES, LOCATION_PREFERENCES


class LocationProfileForm(ListForm):
    css_class = 'shable-form'
    description = TextArea(label='DESCRIZIONE BREVE', css_class='form-control')
    address = TextField(label='INDIRIZZO', css_class='form-control')
    number = TextField(label='NUMERO', css_class='form-control')
    city = TextField(label='CITTA\'', css_class='form-control')
    zip_code = TextField(label='CAP', css_class='form-control')
    food_types = CheckBoxList(label='PREFERENZE ALIMENTARI', options=FOOD_TYPES, css_class='chbx-list')
    preferences = CheckBoxList(label='PREFERENZE TAVOLA', options=LOCATION_PREFERENCES, css_class='chbx-list')
    photos = AjaxManagePhotos(label='FOTO', css_class="ajax_manage_photos",
                              action=json_lurl('/user_profile/location/photos/save'),
                              delete_action=json_lurl('/user_profile/location/photos/remove'),
                              permit_upload=True)
    submit = SubmitButton(value='Salva Tavola', css_class='form-control')
    action = lurl('/user_profile/location/update_details')


class LocationProfileController(BaseController):
    allow_only = predicates.not_anonymous()
    photos = TemporaryPhotosUploader()

    @expose('shable.templates.user_profile.location')
    def index(self):
        user = request.identity['user']
        location = user.location
        validation_error = request.validation['exception']
        if validation_error is not None:
            # Rerendering a form that failed validation,
            # recover the currently uploaded photos.
            fields = validation_error.widget.child.children
            fields.photos.value = {'photos': self.photos.current_photos()}
            value = {}
        else:
            # Rendering a new upload form, start with empty photos bucket
            self.photos.new_bucket()
            value = {'description': location.description, 'address': location.address, 'number': location.number,
                     'city': location.city, 'zip_code': location.zip_code, 'food_types': location.food_types,
                     'preferences': location.preferences,
                     'photos': {'photos': self.photos.recover_photos(getattr(location, 'photos', None))}}
        return {'form': LocationProfileForm, 'value': value}

    @expose()
    def update_details(self, **kw):
        user = request.identity['user']
        bucket = self.photos.get_bucket()
        user.location.photos = bucket.photos
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

        flash('Tavola aggiornata!')
        redirect('/user_profile/location')

