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

"""Module that instantiates our Flask WSGI app and associates all
implemented blueprints in various modules to this app.
"""

from flask import Flask, request

from gd.auth import authenticated_user, NobodyHome
from gd import conf

from gd.admin import admin
from gd.audience import audience
from gd.auth.webapp import auth
from gd.buzz.webapp import buzz
from gd.buzz.facebookapp import fbapp
from gd.govpergunta import govpergunta


app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(buzz, url_prefix='/buzz')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(audience, url_prefix='/audience')
app.register_blueprint(fbapp, url_prefix='/fbapp')
app.register_blueprint(govpergunta, url_prefix='/govpergunta')


# Registering a secret key to be able to work with sessions
app.secret_key = conf.SECRET_KEY


@app.context_processor
def extend_context():
    """This function is a context processor. It injects variables such
    as `user' and `host' variable in all templates that will be rendered
    for this application"""

    context = {}

    # This will be used to bind socket.io client API to our
    # server. Without the port information.
    context['host'] = request.host.split(':')[0]

    # Time to add the `user' var
    try:
        context['user'] = authenticated_user()
    except NobodyHome:
        context['user'] = None

    # Job done!
    return context
