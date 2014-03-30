# -*- coding: utf-8 -*-

"""WebHelpers used in shable."""

#from webhelpers import date, feedgenerator, html, number, misc, text
from markupsafe import Markup
from datetime import datetime
from tg import request
import tg


def current_year():
  now = datetime.now()
  return now.strftime('%Y')

def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)

def user_avatar(user=None):
    if user is None:
        user = request.identity['user']
    if getattr(user, 'avatar', None) is None:
        return 'http://placehold.it/180x180'
    if len(user.avatar) < 1:
        return 'http://placehold.it/180x180'
    return tg.url(user.avatar[0].url, qualified=True)

def user_info():
    return request.identity['user']

def location_image(user=None):
    if user is None:
        user = request.identity['user']
    return tg.url(user.location.photos[0].url, qualified=True)

def meal_image(meal):
    return tg.url(meal.photos[0].url, qualified=True)

def format_date(date):
    return date.strftime('%d-%m-%Y')

def format_price(price):
    return "%0.2f" % price

def genderized(user):
    if user.gender == 'F':
        return 'LA CUOCA'
    return 'IL CUOCO'