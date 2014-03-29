from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm import Mapper
from ming.odm.declarative import MappedClass
from session import DBSession


FOOD_TYPES = ['Pasta', 'Carne', 'Pizza', 'Desert', 'Birra']
LOCATION_PREFERENCES = ['Musica', 'Scambio Multiculturale', 'Fumatori']
SPECIFIC_MEAL = ['Vegano', 'Celiaco', 'Vegetariano']
HOURS = [i for i in range(24)]
MINUTES = [i for i in range(60)]

class Meal(MappedClass):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """
    class __mongometa__:
        session = DBSession
        name = 'meals'

    _id = FieldProperty(s.ObjectId)
    name = FieldProperty(s.String)
    description = FieldProperty(s.String)
    menu = FieldProperty(s.String)
    date = FieldProperty(s.DateTime)
    start_time = FieldProperty(s.Anything)
    end_time = FieldProperty(s.Anything)
    price = FieldProperty(s.Float)
    availability = FieldProperty(s.Int)
    specific_meal = FieldProperty(s.String)
    photos = FieldProperty(s.Anything)
