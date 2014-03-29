# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from axf.widgets.ajax_manage_photos import AjaxManagePhotos
from tg import expose, lurl, redirect, request, validate
from tw2.core import DateTimeValidator
from tw2.forms import ListForm, TextField, SingleSelectField, SubmitButton, TextArea, CalendarDatePicker
from shable.controllers.utils.temporary_photos import TemporaryPhotosUploader
from shable.lib.base import BaseController
from shable.lib.utils import json_lurl
from shable.model import models
from shable.model.models import HOURS, MINUTES, SPECIFIC_MEAL


class NewMealForm(ListForm):
    css_class = 'shable-form'
    name = TextField(label='NOME', css_class='form-control')
    description = TextArea(label='DESCRIZIONE', css_class='form-control')
    menu = TextArea(label='MENU', css_class='form-control')
    date = CalendarDatePicker(label='DATA',
                              validator=DateTimeValidator(format='%d/%m/%Y', required=True,
                                                          min=datetime.strptime('1/1/1970', '%d/%m/%Y')),
                              date_format='%d/%m/%Y',
                              attrs=dict(placeholder="gg/mm/aaaa"),
                              css_class="form-control")
    start_hour = SingleSelectField(label='INIZIO', css_class='form-control small-single-select', options=HOURS)
    start_minute = SingleSelectField(label=None, css_class='form-control small-single-select', options=MINUTES,
                                     container_attrs={'class': 'single-select-hack'})
    end_hour = SingleSelectField(label='FINE', css_class='form-control small-single-select', options=HOURS)
    end_minute = SingleSelectField(label=None, css_class='form-control small-single-select', options=MINUTES,
                                   container_attrs={'class': 'single-select-hack'})
    availability = TextField(label='DISPONIBILITA\'', css_class='form-control')
    specific_meal = SingleSelectField(label='PASTO SPECIFICO', css_class='form-control', options=SPECIFIC_MEAL)
    photos = AjaxManagePhotos(label='FOTO', css_class="ajax_manage_photos",
                              action=json_lurl('/user_profile/meals/photos/save'),
                              delete_action=json_lurl('/user_profile/meals/photos/remove'),
                              permit_upload=True)
    submit = SubmitButton(value='Salva Pasto', css_class='form-control')
    action = lurl('/user_profile/meals/create')


class ManageMealsController(BaseController):
    photos = TemporaryPhotosUploader()

    @expose('shable.templates.user_profile.meals')
    def index(self):
        return {}

    @expose('shable.templates.user_profile.new_meal')
    def new(self):
        return {'form': NewMealForm}

    @validate(NewMealForm, error_handler=new)
    @expose()
    def create(self, **kw):
        user = request.identity['user']
        bucket = self.photos.get_bucket()
        values = kw
        values['photos'] = bucket.photos
        values['availability'] = int(values['availability'])
        print values
        start_time = {'hour', 'minute'}
        values['start_time']['hour'] = values.pop('start_hour')
        values['start_time']['minute'] = values.pop('start_minute')
        values['end_time']['hour'] = values.pop('end_hour')
        values['end_time']['minute'] = values.pop('end_minute')
        print values
        meal = models.Meal(**values)
        user._meals.append(meal._id)

        redirect('/user_profile/meals')