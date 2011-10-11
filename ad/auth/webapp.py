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

from flask import Blueprint, render_template, request, abort
from ad.utils import msg, _
from ad.auth import login


auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static')


@auth.route('/login')
def login_form():
    return render_template('login.html')


@auth.route('/login_json')
def login_json():
    username = request.values.get('username')
    password = request.values.get('password')
    if username and password:
        user = login(username, password)
        if user is None:
            return msg.error(_(u'User or password mismatch'))
        return msg.ok({ 'user': user })
    return msg.error(_(u'Username or password missing'))
