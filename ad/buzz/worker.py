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

import multiprocessing
import Queue

class Worker(multiprocessing.Process):
    def __init__(self, queue):
        self.queue = queue
        self.alive = False
        multiprocessing.Process.__init__(self)

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
                audience = self.queue.get_nowait()
            except Queue.Empty:
                try:
                    time.sleep(3)
                except KeyboardInterrupt:
                    self.alive = False
                continue
