from tg import expose, request, lurl, flash
from tw2.forms import ListForm, TextField, SubmitButton, SingleSelectField, CalendarDatePicker
from shable.lib.base import BaseController
from shable.lib.utils import coordinate
from shable.model import User


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
    quando = TextField(label='', placeholder='Quando', css_class='form-control')

    submit = None
    action = lurl('/search/results')


class SearchController(BaseController):

    @expose('shable.templates.search')
    def index(self):

        return {'form': SearchForm, 'value': {}}



    @expose('shable.templates.results')
    def query(self, **kw):
        position = coordinate(kw.get('place'))

        answer = User.query.find({})


        flash("Query done")
        return {'form': SearchResultForm, 'value': {}}



