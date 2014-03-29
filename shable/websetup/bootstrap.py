# -*- coding: utf-8 -*-
"""Setup the shable application"""
from __future__ import print_function

import logging
from tg import config
from shable import model

def bootstrap(command, conf, vars):
    """Place any commands to setup shable here"""

    # <websetup.bootstrap.before.auth
    g = model.Group()
    g.group_name = 'managers'
    g.display_name = 'Managers Group'

    p = model.Permission()
    p.permission_name = 'manage'
    p.description = 'This permission give an administrative right to the bearer'
    p.groups = [g]

    u = model.User()
    u.user_name = 'manager'
    u.name = 'Example'
    u.surname = 'manager'
    u.email_address = 'manager@shable.co'
    u.groups = [g]
    u.password = 'managepass'

    u1 = model.User()
    u1.user_name = 'gasba'
    u1.name = 'Simone'
    u1.surname = 'Gasbarroni'
    u1.email_address = 'gas@shable.co'
    u1.password = '123'

    u1 = model.User()
    u1.user_name = 'user'
    u1.name = 'Example'
    u1.surname = 'User'
    u1.email_address = 'user@shable.co'
    u1.password = '123'


    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
