# coding=utf-8
from __future__ import unicode_literals
from axf.widgets.ajax_manage_photos import AjaxManagePhotos

from tg import predicates, expose, lurl, redirect, request, flash
from tw2.forms import TableForm, ListForm, TextField, SingleSelectField, SubmitButton
from shable.controllers.user_profile.location import LocationProfileController
from shable.controllers.utils.temporary_photos import TemporaryPhotosUploader
from shable.lib.base import BaseController
from shable.lib.utils import json_lurl


class UserProfileForm(ListForm):
    css_class = 'shable-form'
    name = TextField(label='NOME', css_class='form-control')
    surname = TextField(label='COGNOME', css_class='form-control')
    gender = SingleSelectField(label='SESSO', css_class='form-control', options=['M', 'F'])
    submit = SubmitButton(value='Salva Profilo', css_class='form-control')
    avatar = AjaxManagePhotos(label='AVATAR', css_class="ajax_manage_photos",
                              action=json_lurl('/user_profile/photos/save'),
                              delete_action=json_lurl('/user_profile/photos/remove'),
                              permit_upload=True)
    action = lurl('/user_profile/update_profile')


class UserProfileController(BaseController):
    allow_only = predicates.not_anonymous()
    location = LocationProfileController()
    photos = TemporaryPhotosUploader()


    @expose('shable.templates.user_profile.index')
    def index(self):
        user = request.identity['user']
        validation_error = request.validation['exception']
        if validation_error is not None:
            # Rerendering a form that failed validation,
            # recover the currently uploaded photos.
            fields = validation_error.widget.child.children
            fields.avatar.value = {'photos': self.photos.current_photos()}
            value = {}
        else:
            # Rendering a new upload form, start with empty photos bucket
            self.photos.new_bucket()
            value = {'name': user.name, 'surname': user.surname, 'gender': user.gender,
                     'avatar': {'photos': self.photos.recover_photos(getattr(user, 'avatar', None))}}

        return {'form': UserProfileForm, 'value': value}

    @expose()
    def update_profile(self, **kw):
        user = request.identity['user']
        bucket = self.photos.get_bucket()
        user.avatar = bucket.photos
        user.name = kw['name']
        user.surname = kw['surname']
        user.gender = kw['gender']
        flash('Profilo aggiornato!')
        redirect('/user_profile')


