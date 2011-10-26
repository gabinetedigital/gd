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
from sqlalchemy.orm.exc import NoResultFound

from ad.utils import phpass, msg, _
from ad.model import User, session as dbsession


class AuthError(Exception):
    """Base class for login errors"""


class UserNotFound(AuthError):
    """Exception raised when an user is not found by its username"""


class UserAndPasswordMissmatch(AuthError):
    """Exception raised when user and password missmatches"""


class NobodyHome(AuthError):
    """Exception raised when the trying to get the authenticated user
    with nobody logged in"""


class UserExists(AuthError):
    """Exception raised when the user already exists in the database"""


class EmailAddressExists(AuthError):
    """Exception raised when an email address already exists in the
    database"""



def is_authenticated():
    """Boolean func that says if the current user is authenticated"""
    return 'username' in session


def authenticated_user():
    """Returns the authenticated user instance"""
    try:
        return User.query.filter_by(username=session['username']).one()
    except KeyError:
        raise NobodyHome()


def login(username, password):
    """Logs a user in the current session"""
    # Testing if the user exists
    try:
        user = User.query.filter_by(username=username).one()
    except NoResultFound:
        raise UserNotFound()
    return login_user_instance(user, password)


def login_user_instance(user, password):
    """Logs an user instance in, instead of receiving it's username as a
    string"""
    # Testing user's password
    hasher = phpass.PasswordHash(8, True)
    if not hasher.check_password(password, user.password):
        raise UserAndPasswordMissmatch()

    # Everything seems to be ok here, let's register the user in our
    # session and return its data (but the password, of course) to the
    # caller.
    session['username'] = user.username
    return user.public_dict()


def logout():
    """Logs the current online user out"""
    if is_authenticated():
        session.pop('username')


class checkroles(object):
    """Decorator factory to check if an user accessing a flask
    controller has one of the received roles"""
    def __init__(self, roles, redirect_on_error=True):
        self.roles = roles
        self.redirect_on_error = redirect_on_error

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper that actually tests the user permissions"""
            if not is_authenticated() and self.redirect_on_error:
                return redirect(
                    '%s?next=%s' % (url_for('admin.login'), request.url))
            elif not is_authenticated():
                return msg.error(
                    _(u'No user authenticated.'),
                    NobodyHome.__name__)
            try:
                user = authenticated_user()
            except AuthError, exc:
                return msg.error(
                    unicode(exc.message),
                    exc.__class__.__name__)
            if not user.has_roles(self.roles):
                return msg.error(
                    _(u'The currently logged user don\'t have suficient '
                      u'privileges to access this resource'))
            return func(*args, **kwargs)
        return wrapper


def create_user(name, username, password, email, meta=None):
    """Create a new user in the database"""
    # There will be one and only one user with a given username
    if User.query.filter_by(username=username).count():
        raise UserExists()
    if User.query.filter_by(email=email).count():
        raise EmailAddressExists()

    # Creating an user instance and getting its id by commiting the
    # chage to the database
    user = User(
        name=name, username=username, password=password, email=email)
    dbsession.commit()

    # Time to save all meta attributes that we received
    for key, value in (meta or {}).items():
        UserMeta(user_id=user.id, meta_key=key, meta_value=value)
    dbsession.commit()

    return user
