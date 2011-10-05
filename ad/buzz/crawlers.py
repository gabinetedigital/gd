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

"""This module is intended to provide clients used to track some
profiles and hashtags in different social networks.
"""

from urllib import urlopen
from time import sleep
from json import loads
from tweetstream import FilterStream, ConnectionError

from ad.model import Buzz, BuzzType, get_or_create

USER_API_URL = 'http://api.twitter.com/1/users/show.json?screen_name=%s'

class Twitter(object):
    """A twitter stream client that saves tweets from some given
    `profiles' and `hashtags'.
    """
    def __init__(self, profiles, hashtags):
        self.profiles = profiles
        self.hashtags = hashtags
        self.profileids = []
        self.resolve_profile_ids()

    def resolve_profile_ids(self):
        """We need to resolve the screen names to user ids to use the
        twitter stream API. This method does this job by requesting the
        `USER_API_URL' and getting the `id' property from the returned
        json content.
        """
        for screen_name in self.profiles:
            self.profileids.append(
                loads(urlopen(USER_API_URL % screen_name).read())['id'])

    def process(self):
        """Here's the place that we actually call the stream API and
        capture found tweets.

        Each time we receive a new tweet, we create a `Buzz' instance
        with it's owner and content info and then yield it to the
        caller. None is saved to the database here.
        """
        print 'processing %s, %s' % (self.profileids, self.hashtags)
        try:
            stream = FilterStream(
                'blah220214', 'blah220214blah220214blah220214',
                follow=self.profileids, track=self.hashtags)
        except ConnectionError:
            # Something got screwed, let's try some seconds late.
            # FIXME: We really should limit the number of tries here and
            # warning the sysadmin that something is wrong.
            sleep(3)
            self.process()

        for tweet in stream:
            # We're creating a new entry in our buzz entity for each
            # tweet received. We are also setting this buzz as a twitter
            # one and yielding it to the caller that will be the
            # responsible for saving it in the database.
            buzz = Buzz(
                owner_nick=tweet['user']['screen_name'],
                owner_avatar=tweet['user']['profile_image_url'],
                content=tweet['text'])
            buzz.type_ = get_or_create(BuzzType, name=u'twitter')[0]
            yield buzz
