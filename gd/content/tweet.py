# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Thiago Silva <thiago@metareload.com>
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

"""This is a simple module that takes care about the twitter integration
on our home page
"""

from gd.model import MayorTweet


def set_mayor_last_tweet(data):
    """Save the mayor tweet when it comes from our bot!"""
    MayorTweet.save_tweet(data)


def get_mayor_last_tweet():
    """Returns the text of the last tweet of the mayor"""
    try:
        return MayorTweet.get_current().text
    except AttributeError:
        return u''

