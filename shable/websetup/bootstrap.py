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
    u.display_name = 'Example manager'
    u.email_address = 'manager@somedomain.com'
    u.groups = [g]
    u.password = 'managepass'

    u1 = model.User()
    u1.user_name = 'editor'
    u1.display_name = 'Example editor'
    u1.email_address = 'editor@somedomain.com'
    u1.password = 'editpass'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
