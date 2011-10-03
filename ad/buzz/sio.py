# Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
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

from flask import current_app
from gevent_zeromq import zmq
from gevent import spawn, sleep

from ad.utils import dumps

class BuzzApp(object):
    """A WSGI application that serves socketio and proxies all other
    path calls to the main Flask app.
    """
    def __init__(self, app):
        self.context = zmq.Context()
        self.app = app
        self.set_server()

    def set_server(self):
        self.app.server = self.context.socket(zmq.PUB)
        self.app.server.bind('tcp://127.0.0.1:6000')
        self.app.send = lambda msg, data: self.send(msg, data)

    def setup(self):
        spawn(self.server, self.context)

    def send(self, message, data):
        self.app.server.send(dumps({ 'message': message, 'data': data }))

    def __call__(self, environ, start_response):
        # This app just handles socketio stuff, so we need to pass all
        # other requests to the flask app
        if not environ['PATH_INFO'].startswith('/socket.io'):
            return self.app(environ, start_response)

        socketio = environ['socketio']
        sock = self.context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect('inproc://queue')
        while True:
            msg = sock.recv()
            socketio.send(msg)


def send(msg, data):
    current_app.send(msg, data)
