import datetime
from tg import expose, request, lurl, flash
from tw2.forms import ListForm, TextField, SubmitButton, SingleSelectField, CalendarDatePicker
from shable.lib.base import BaseController
from shable.lib.utils import coordinate, earth_radius_km
from shable.model import User, Meal
import json


class SearchForm(ListForm):
    css_class = 'shable-form'

    place = TextField(label='', placeholder='Dove', css_class='form-control')
    when = CalendarDatePicker(label='', placeholder='Quando', css_class='form-control')
    guests = SingleSelectField(label='', placeholder='#Ospiti', css_class='form-control', options = ["1","2","3","4","5","6"])

    submit = SubmitButton(value='Cerca', css_class='form-control')
    action = lurl('/search/query')


class SearchResultForm(ListForm):
    css_class = 'shable-form'

    place = TextField(label='', placeholder='Dove', css_class='form-control')
    when = TextField(label='', placeholder='Quando', css_class='form-control')

    submit = None
    action = lurl('/search/results')


class SearchController(BaseController):

    @expose('shable.templates.search')
    def index(self):

        return {'form': SearchForm, 'value': {}}



    @expose('shable.templates.results')
    def query(self, **kw):

        position = coordinate(kw.get('place'))

        if kw.get('when'):
            date = datetime.datetime.strptime(kw.get('when'),"%m/%d/%Y")

        else:
            date = datetime.datetime.utcnow()
        if kw.get('guests'):
            eater = int(kw.get('guests'))
        else:
            eater = 1
        search_results = [u.user_id for u in Meal.query.find({'availability':{'$gte': eater},'date' :{'$gte': date} }).all()]

        users = User.query.find({'_id': {'$in': search_results},
                                 'position': {'$geoWithin':
                                                  {'$centerSphere': [position, 10 / earth_radius_km] }} }).all()

        flash("Query done")
        print  users
        geo_points_json = []
        geo_points_json.append(position)
        geo_points_json = []#[ u.location.position for u in users ]

        geo_points_json.append([ 7, 43])
        geo_points_json.append([7.33, 43.33])

        return dict(form=SearchResultForm, value= users, geo_points_json=json.dumps(geo_points_json))




