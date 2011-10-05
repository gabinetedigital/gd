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

"""Implements the WSGI app that handles socketio stuff and a bus service
to provide a comunication layer for the components of our app.
"""

from flask import current_app
from gevent_zeromq import zmq
from gevent import spawn

from ad.utils import dumps


class BuzzApp(object):
    """A WSGI application that serves socketio and proxies all other
    path calls to the main Flask app.
    """
    def __init__(self, app=None):
        self.context = zmq.Context()
        self.app = app
        self.setup()

    def server(self, ctx):
        """Starts the internal server that publishes messages for the
        processes running our crawlers. And also proxies received
        messages for our socketio message queue.
        """
        self.app.server = ctx.socket(zmq.PUB)
        self.app.server.bind('tcp://127.0.0.1:6000')
        self.app.send = lambda msg, data: self.send(msg, data)

        # Things relative to socketio
        incoming = ctx.socket(zmq.PULL)
        incoming.bind('tcp://127.0.0.1:6001')

        publishing = self.context.socket(zmq.PUB)
        publishing.bind('inproc://queue')
        while True:
            msg = incoming.recv()
            publishing.send(msg)

    def setup(self):
        """Spawns the internal server through gevent"""
        spawn(self.server, self.context)

    def send(self, message, data):
        """Sends a message to all connected clients"""
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
    """Wrapper to send messages to all our connected clients if used
    from the webapp. Otherwise, sends a message to the socketio bus
    """
    if bool(current_app):
        return current_app.send(msg, data)

    # This code will only run when no app is binded. Which means we
    # don't need to provide any socketio thing
    server = zmq.Context().socket(zmq.PUSH)
    server.connect('tcp://127.0.0.1:6001')
    server.send(dumps({ 'message': msg, 'data': data }))
    server.close()
