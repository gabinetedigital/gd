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

from multiprocessing import Queue, cpu_count
from time import sleep
from ad.model import Audience
from ad.buzz.worker import Worker

class Server(object):
    def __init__(self, workers=cpu_count()):
        # Flag to define if our server is up and running or not
        self.alive = False

        # This is the queue that holds Audiences that are being
        # processed
        self.queue = Queue(0)

        # Workers that actually process audience instances
        self.workers = []
        for i in range(workers):
            self.workers.append(Worker(self.queue))
            self.workers[i].start()

        # Instances being managed. We must avoid processing the same
        # audience twice in the same session
        self.instances = []

    def start(self):
        self.alive = True
        self.run()

    def run(self):
        """Finds all visible audiences and add them to be watched
        """
        while self.alive:
            # Looking for all visible audiences that are out of our
            # queue and adding them to be processed.
            query = Audience.query \
                .filter(~Audience.id.in_(self.instances)) \
                .filter_by(visible=True) \
                .all()
            for i in query:
                self.queue.put(i)
                self.instances.append(i.id)
            print query
            sleep(10)


if __name__ == '__main__':
    Server().start()
