# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Module that holds all authentication specific stuff

The login/logout functionalities are indeed implemented here, but if
you're looking for the login form (or for the logut controller), please
refer to the `ad.admin' module.
"""

from flask import request, session, redirect, url_for
from functools import wraps


def is_authenticated():
    """Boolean func that says if the current user is authenticated"""
    return 'username' in session


def login(username, password):
    """Logs a user in"""
    session['username'] = username


def logout():
    """Logs the current online user out"""
    if is_authenticated():
        session.pop('username')


class checkpermissions(object):
    """Decorator factory to check if an user accessing a flask
    controller has a specific set of permissions"""
    def __init__(self, permissions):
        self.permissions = permissions

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper that actually tests the user permissions"""
            if not is_authenticated():
                return redirect(
                    '%s?next=%s' % (url_for('admin.login'), request.url))
            return func(*args, **kwargs)
        return wrapper
