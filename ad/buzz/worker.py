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

"""Module that implements a worker that will call social network
crawlers in separated processes.
"""

from time import sleep
from multiprocessing import Process
import Queue

from ad.buzz.sio import notify_new_buzz
from ad.buzz.crawlers import Twitter
from ad.model import Audience, session

class Worker(Process):
    """Class that inherits from the `multiprocessing.Process' class to
    be executed in a separated process.

    When it is executed, it looks for an audience given the id received
    from the queue set by the server and then start looking for messages
    in the supported social networks and save them in the database.
    """
    def __init__(self, queue):
        self.queue = queue
        self.alive = False
        Process.__init__(self)

    def start(self):
        """Sets the internal alive flag to true and starts the proccess.
        """
        self.alive = True
        super(Worker, self).start()

    def stop(self):
        """Sets the internal alive flag to false.
        """
        self.alive = False

    def run(self):
        """Starts a social network crawler
        """
        while self.alive:
            try:
                audience = Audience.query.get(self.queue.get_nowait())
                profiles, hashtags = [], []
                for i in audience.terms:
                    term = str(i)
                    if term.startswith('@'):
                        profiles.append(term)
                    else:
                        hashtags.append(term)
                for buzz in Twitter(profiles, hashtags).process():
                    audience.buzzes.append(buzz)
                    session.commit()
                    notify_new_buzz(buzz)

            except Queue.Empty:
                try:
                    sleep(3)
                except KeyboardInterrupt:
                    self.alive = False
                continue
