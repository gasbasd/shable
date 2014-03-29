# -*- coding: utf-8 -*-
"""The application's model objects"""

import ming.odm
from session import mainsession, DBSession
from pymongo import GEO2D
from pymongo.errors import OperationFailure

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    mainsession.bind = engine
    ming.odm.Mapper.compile_all()

    for mapper in ming.odm.Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)

    try:
        mainsession.db.tg_user.drop_index([('location.position', GEO2D)])
    except OperationFailure:
        pass

    mainsession.db.tg_user.ensure_index([('location.position', GEO2D)])

# Import your model modules here.
from shable.model.auth import User, Group, Permission
from shable.model.temporary_photos import TemporaryPhotosBucket
from shable.model.models import Meal

