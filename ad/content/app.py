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

if __name__ == '__main__':
    import sys
    # Ugly but will help us to run the application in debug mode when we
    # need. This way, the socketio and all the intercommunication stuff
    # will not be started. The ad-d script will be responsible for that
    # step when it is needed.
    sys.path.append('..')


from flask import Flask, request
from ad.admin import admin
from ad.audience import audience
from ad.auth.webapp import auth
from ad.buzz.webapp import buzz
from ad.buzz.facebookapp import fbapp

from ad.auth import authenticated_user, NobodyHome
from ad import conf

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(buzz, url_prefix='/buzz')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(audience, url_prefix='/audience')
app.register_blueprint(fbapp, url_prefix='/fbapp')


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


# Registering a secret key to be able to work with sessions
import os
app.secret_key = conf.SECRET_KEY


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
