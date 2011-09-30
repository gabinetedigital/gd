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

"""This module is responsible for seeking for terms in social networks
like twitter, identi.ca and facebook.

After finding things, it stores in a database entity declared in the
`ad.model' module to make the found information available for all
modules of this application.
"""

from flask import Blueprint, render_template, request

buzz = Blueprint(
    'buzz', __name__,
    template_folder='templates',
    static_folder='static')


@buzz.route('/')
def index():
    # Removing the port from host info. This will be used to bind
    # socket.io client API to our server.
    host = request.host.split(':')[0]
    return render_template('buzz/index.html', host=host)
