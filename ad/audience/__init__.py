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

audience = Blueprint(
    'audience', __name__,
    template_folder='templates',
    static_folder='static')

@audience.route('/<int:aid>')
def index(aid):
    # Removing the port from host info. This will be used to bind
    # socket.io client API to our server.
    host = request.host.split(':')[0]
    inst = Audience.query.get(aid)
    inst_t = Term.query.filter_by(main=1,audience=inst).one()
    return render_template(
        '/index.html', inst=inst, inst_t=inst_t, host=host)
