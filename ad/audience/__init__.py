# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
#   Author: Rodrigo Sebastiao da Rosa <rodrigo-rosa@procergs.rs.gov.br>
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

"""Module that uses the Template and Model APIs to build the Audience web
interface.
"""

from flask import Blueprint, render_template, request
from ad.model import Audience, Term
from ad.utils import dumps

audience = Blueprint(
    'audience', __name__,
    template_folder='templates',
    static_folder='static')

@audience.route('/<int:aid>')
def index(aid):
    """Renders an audience with its public template"""
    # Removing the port from host info. This will be used to bind
    # socket.io client API to our server.
    host = request.host.split(':')[0]
    audience = Audience.query.get(aid)
    return render_template(
        '/index.html', audience=audience, host=host)


@audience.route('/<int:aid>/public_buzz')
def public_buzz(aid):
    """Returns the public buzz of an audience in JSON format"""
    return dumps([buzz.to_dict(deep={ 'type_': {} })
                  for buzz in Audience.query.get(aid).get_public_buzz()])


@audience.route('/<int:aid>/moderated_buzz')
def moderated_buzz(aid):
    """Returns the moderated buzz of an audience in JSON format"""
    return dumps([buzz.to_dict(deep={ 'type_': {} })
                  for buzz in Audience.query.get(aid).get_moderated_buzz()])
