import datetime
from tg import expose, request, lurl, flash
from tw2.forms import ListForm, TextField, SubmitButton, SingleSelectField, CalendarDatePicker
from shable.lib.base import BaseController
from shable.lib.utils import coordinate, earth_radius_km
from shable.model import User, Meal
import json


class SearchForm(ListForm):
    css_class = 'shable-form search-form'

    place = TextField(label='', placeholder='Dove', css_class='form-control shable-search-field',
                      container_attrs={'class': 'shable-search-field-container'})
    when = CalendarDatePicker(label='', attrs=dict(placeholder="Quando"),
                              css_class='form-control shable-search-field calendar-field',
                              container_attrs={'class': 'shable-search-field-container'})
    guests = SingleSelectField(label='', placeholder='#Ospiti', css_class='form-control shable-search-field',
                               options=["1","2","3","4","5","6"],
                               container_attrs={'class': 'shable-search-field-container'})

    submit = SubmitButton(value='Cerca', css_class='shable-search-submit')
    action = lurl('/search/query')


class SearchResultForm(ListForm):
    css_class = 'shable-form'

    place = TextField(label=None, placeholder='Dove', css_class='form-control')
    when = CalendarDatePicker(label=None, attrs=dict(placeholder="Quando"),
                              css_class='form-control calendar-field')
    guests = SingleSelectField(label=None, css_class='form-control',
                               options = ["Quanti","1","2","3","4","5","6"])

    submit = SubmitButton(value='Cerca', css_class='shable-detailed-search-submit')
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
        search_results = [u.user_id for u in Meal.query.find({'availability':{'$gte': eater},
                                                              'date' :{'$lte': date+ datetime.timedelta(hours=23, minutes=59, seconds= 59)
                                                                  , '$gte': date} }).all()]
        #date += datetime.timedelta(hours=23, minutes=59, seconds= 59)
        users = User.query.find({'_id': {'$in': search_results},
                                 'location.position': {'$geoWithin':
                                                  {'$centerSphere': [position, 10 / earth_radius_km] }} }).all()

        geo_points_json = []
        geo_points_json.append(position)
        for u in users:
            geo_points_json.append(u.location.position)

        geo_points_description = []
        geo_points_description.append("Need it not used!")
        for u in users:
            geo_points_description.append(u.name +": "+ u.location.description)

        return dict(form=SearchResultForm, value= users,
                    geo_points_json=json.dumps(geo_points_json),
                    geo_points_description =json.dumps(geo_points_description))




