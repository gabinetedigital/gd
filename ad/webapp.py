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


from flask import Flask
from ad.admin import admin
from ad.audience import audience
from ad.buzz.webapp import buzz
from ad.buzz.facebookapp import fbapp

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(buzz, url_prefix='/buzz')
app.register_blueprint(audience, url_prefix='/audience')
app.register_blueprint(fbapp, url_prefix='/fbapp')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
