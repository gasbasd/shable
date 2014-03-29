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

def user_avatar():
    user = request.identity['user']
    if getattr(user, 'avatar', None) is None:
        return 'http://placehold.it/180x180'
    return tg.url(user.avatar[0].url, qualified=True)

def user_info():
    return request.identity['user']