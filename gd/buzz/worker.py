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

from multiprocessing import Process
from gd.model import Audience, session


class Worker(Process):
    """Object that actually follows the stream of a social network.

    To create a new `Worker', you need to inform the id of the audience
    and which social network you want to follow. Just like this::

      >>> Worker(1, Twitter).start()

    The second param is a class that can be found in the
    `ad.buzz.crawlers' module.
    """
    def __init__(self, aid, job):
        self.aid = aid
        self.job = job
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
            audience = Audience.query.get(self.aid)
            profiles, hashtags = [], []
            for i in audience.terms:
                term = str(i)
                if term.startswith('@'):
                    profiles.append(term)
                else:
                    hashtags.append(term)
            try:
                for buzz in self.job(profiles, hashtags).process():
                    buzz.audience = audience
                    audience.buzzes.append(buzz)
                    session.commit()
            except KeyboardInterrupt:
                self.alive = False
