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

"""The buzzwatcher server


This component is a server that is subscribed to the internal message
system, based on the amazing zmq framework. It waits for messages of the
`new_audience' kind. When one of them arives, a new worker is created
for each social network that we need to watch.

Each worker created is binded to the audience id, which makes easy to
know if an audience is being watched or not.

Here's the flow::


  [ new audience ] -> [ server loop ] ----> identica worker
                                      \
                                        --> twitter worker
                                        \
                                         -> yet another social network
"""

import zmq
from json import loads

from gd.model import Audience
from gd.buzz.worker import Worker
from gd.buzz.crawlers import Twitter


class Server(object):
    """This class is responsible for queueing the process of tracking
    social network buzz about an Audience.

    Specifically, this server looks for audiences added to our database
    from time to time and when it finds one that is `visible', it's id
    is added to a queue that will be processed by workers.
    """
    def __init__(self):
        # Flag to define if our server is up and running or not
        self.alive = False

        # Workers that actually process audience instances. It's a
        # dictionary that each key is the ID of an audience and the
        # value of such a key is a list with workers.
        self.workers = {}

        # Zmq context
        self.context = zmq.Context()

    def start(self):
        """Just starts our server
        """
        self.alive = True
        self.run()

    def process_audience(self, aid):
        """Receives an audience id and creates a new worker for each
        social network that should be followed for an audience."""

        # Watching all social networks we need here. If
        # you're going to implement a new crawler, it's the
        # best place to run it.
        worker = Worker(aid, Twitter)
        worker.start()

        # Saving the just created worker on our workers list
        # based on the audience id
        workers = self.workers.get(aid)
        if workers is None:
            self.workers[aid] = []
            self.workers[aid].append(worker)
        

    def get_initials(self):
        """Finds all visible audiences and add them to be watched
        """
        query = Audience.query \
            .filter_by(visible=True) \
            .all()
        for i in query:
            self.process_audience(i.id)

    def run(self):
        """Waits for the `new_audience' message from the bus service
        and, when it comes, calls the `self.process_audience()' method
        for it.
        """
        self.get_initials()

        subscriber = self.context.socket(zmq.SUB)
        subscriber.setsockopt(zmq.SUBSCRIBE, '')
        subscriber.connect('tcp://127.0.0.1:6000')

        while self.alive:
            try:
                msg = loads(subscriber.recv())
            except KeyboardInterrupt:
                break

            # We're waiting for a single kind of message, that brings a
            # new audience to be watched.
            if msg['message'] == 'new_audience':
                self.process_audience(msg['data']['id'])


if __name__ == '__main__':
    Server().start()
