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

"""Web application definitions for the `auth' module"""

from flask import Blueprint, render_template, request
from ad.utils import msg, _
from ad.auth import forms
from ad import auth as authapi


auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static')


@auth.route('/login')
def login_form():
    """Renders the login form"""
    return render_template('login.html')


@auth.route('/signup')
def signup_form():
    """Renders the signup form"""
    form = forms.SignupForm()
    return render_template('signup.html', form=form)


@auth.route('/login_json', methods=('POST',))
def login_json():
    """Logs the user in (through ajax) and returns the user object in
    JSON format"""
    username = request.values.get('username')
    password = request.values.get('password')
    if username and password:
        try:
            user = authapi.login(username, password)
        except authapi.UserNotFound:
            return msg.error(_(u'User does not exist'), 'UserNotFound')
        except authapi.UserAndPasswordMissmatch:
            return msg.error(_(u'User or password mismatch'),
                             'UserAndPasswordMissmatch')
        return msg.ok({ 'user': user })
    return msg.error(_(u'Username or password missing'), 'EmptyFields')


@auth.route('/logout_json')
def logout_json():
    """Logs the user out and returns an ok message"""
    authapi.logout()
    return msg.ok(_(u'User loged out'))
