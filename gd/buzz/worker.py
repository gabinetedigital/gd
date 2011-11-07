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

from traceback import print_exc
from multiprocessing import Process
from gd.model import Audience, session, set_mayor_last_tweet

# shitty mess'up class ahead
from urllib import urlopen
from time import sleep
from json import loads
from tweetstream import FilterStream, ConnectionError
from gd import conf

TWITTER_JSON_TIMELINE_URL = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s"

class MayorWatcher(Process):
    def __init__(self):
        self.alive = False
        Process.__init__(self)

    def start(self):
        """Sets the internal alive flag to true and starts the proccess.
        """
        self.alive = True
        super(MayorWatcher, self).start()

    def stop(self):
        """Sets the internal alive flag to false.
        """
        self.alive = False

    def run(self):
        """Starts a social network crawler
        """
        self.process()

    def save_current(self):
        """Opens the twitter api requesting the last tweet of the
        configured account"""
        json = urlopen(
            TWITTER_JSON_TIMELINE_URL %
            conf.TWITTER_MAYOR_USERNAME).read()

        message = loads(json)
        # Making sure twitter will let me watch the mayor!
        if 'error' not in message:
            set_mayor_last_tweet(message[0]['text'])

    def process(self):
        """this is supposed to update the last micro-post/status from a
        twitter account so it appears on the front-page of the site.
        Therefore, we don't really need real-time feedback"""
        while self.alive:
            try:
                self.save_current()
                sleep(60 * 8)   # Waiting 5 minutes before trying again
            except KeyboardInterrupt:
                self.alive = False
            except Exception, exc:
                print '(%s) uops...something wrong. trying again soon.' % (
                    exc.__class__.__name__)
                print_exc()


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
