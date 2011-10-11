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
from ad import auth as authapi


auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static')


@auth.route('/login')
def login_form():
    """Renders the login form"""
    return render_template('login.html')


@auth.route('/login_json')
def login_json():
    """Logs the user in (through ajax) and returns the user object in
    JSON format"""
    username = request.values.get('username')
    password = request.values.get('password')
    if username and password:
        try:
            user = authapi.login(username, password)
        except authapi.UserNotFound:
            return msg.error(_(u'User does not exist'))
        except authapi.UserAndPasswordMissmatch:
            return msg.error(_(u'User or password mismatch'))
        return msg.ok({ 'user': user })
    return msg.error(_(u'Username or password missing'))
