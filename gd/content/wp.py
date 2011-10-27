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

"""Module to carry about all interaction between wordpress XMLRPC
interface and our system.
"""

from xmlrpclib import Server
from datetime import datetime

from flask import url_for
from gd import conf


class Wordpress(object):
    """Wordpress XMLRPC client"""
    def __init__(self, address, blogid, user, password):
        self.blogid = blogid
        self.address = address
        self.user = user
        self.password = password
        self.server = Server(self.address)

    def wrap_post(self, data):
        """Wrapps a dictionary that contains data that represents a
        wordpress post into a python class with some helper methods"""
        return Post(data)

    def wrap(self, method):
        """Wrapper that decorates XMLRPC methods that needs the user,
        password and blog id to be passed before anything"""
        def wrapper(*args, **kwargs):
            # Yes, I'm aware that `kwargs' is not being expanded when
            # called in the next line. The params are being sent packed
            # to the XMLRPC server and there they'll be expanded.  Maybe
            # it will change in the future, if I find any function that
            # doesn't fit this strategy
            return method(self.user, self.password, kwargs, *args)
        return wrapper

    def __getattribute__(self, attr):
        try:
            return super(Wordpress, self).__getattribute__(attr)
        except AttributeError:
            return self.wrap(getattr(self.server.exapi, attr))


class Post(object):
    """Wordpress post wrapper class

    This class that makes it more natural and easy to work with posts
    received from the wordpress source in a dictionary format."""
    def __init__(self, data):
        self.data = data

    def __getattribute__(self, attr):
        try:
            return super(Post, self).__getattribute__(attr)
        except AttributeError:
            return self.data[attr]

    @property
    def permalink(self):
        """Returns the permanent link for this post"""
        return url_for('post', pid=self.id)

    def has_category(self, slug):
        """Returns true if the post has a given category"""
        return bool([i for i in self.data['categories'] if i['slug'] == slug])


wordpress = Wordpress(
    conf.WORDPRESS_XMLRPC, conf.WORDPRESS_BLOGID,
    conf.WORDPRESS_USER, conf.WORDPRESS_PASSWORD
)
