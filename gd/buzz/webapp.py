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

"""Some web views used in the buzz implementation.
"""

from flask import Blueprint, render_template, request
from gd.model import Audience, Buzz, BuzzType, session, get_or_create
from gd.utils import msg
from gd import auth


buzz = Blueprint(
    'buzz', __name__,
    template_folder='templates',
    static_folder='static')


@buzz.route('/')
def index():
    """Shows socket io interation. For debugging purposes at the moment.
    """
    return render_template('buzz/index.html')


@buzz.route('/post', methods=('POST',))
@auth.checkroles(['administrator', 'subscriber'], redirect_on_error=False)
def post():
    """When ready, this method will post contributions from users that
    choosen to use our internal message service instead of twitter,
    identica or whatever."""
    audience = Audience.get(request.values.get('aid'))
    newbuzz = Buzz(
        owner_nick=auth.authenticated_user().display_name,
        owner_avatar=u'',
        user=auth.authenticated_user(),
        content=request.values.get('message')[:300],
        type_=get_or_create(BuzzType, name=u'site')[0])
    newbuzz.audience = audience
    session.commit()
    return msg.ok(_('Notice posted successfuly. Please wait a few while '
                    'your message is approved.'))
