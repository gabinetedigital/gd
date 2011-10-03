# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Rodrigo Sebastiao da Rosa <rodrigo-rosa@procergs.rs.gov.br>
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

from datetime import datetime
from elixir import *
import elixir.events
import os

from ad.buzz import sio

class Term(Entity):
    using_options(shortnames=True)

    hashtag = Field(Unicode(45))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode)
    main = Field(Boolean)
    audience = ManyToOne('Audience')

    def __str__(self):
        return self.hashtag

class Audience(Entity):
    using_options(shortnames=True)

    title = Field(Unicode(250))
    subject = Field(UnicodeText)
    description = Field(UnicodeText)
    date = Field(DateTime)
    creation_date = Field(DateTime, default=datetime.now)
    terms = OneToMany('Term')
    visible = Field(Boolean, default=True)
    owner = Field(Unicode)
    embed = Field(Unicode(150))
    buzzes = OneToMany('Buzz')

    def __str__(self):
        return '<%s "%s" (%d)>' % (
            self.__class__.__name__, self.description, self.date)

    @elixir.events.after_insert
    def notify(self):
        sio.send('new_audience', { 'id': self.id })


class Buzz(Entity):
    using_options(shortnames=True)

    owner_nick = Field(Unicode)
    owner_email = Field(Unicode)
    content = Field(UnicodeText)
    status = Field(Enum(u'inserted', u'approved', u'selected', u'published'), default=u'inserted')
    creation_date = Field(DateTime, default=datetime.now)
    audience = ManyToOne('Audience')
    type_ = ManyToOne('BuzzType')

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.content)


class BuzzType(Entity):
    using_options(shortnames=True)

    name = Field(UnicodeText)
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode)
    buzzes = OneToMany('Buzz')

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.name)

# Helper functions

def get_or_create(model, **kwargs):
    """Helper function to search for an object or create it otherwise,
    based on the Django's Model.get_or_create() method.
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {}
        for k, v in kwargs.iteritems():
            params[k] = v
        instance = model(**params)
        session.add(instance)
        return instance, True


# Database setup

metadata.bind = "sqlite:///%s" % os.path.join(
    os.path.dirname(__file__), 'var', 'db')
metadata.bind.echo = True
setup_all(__name__ == '__main__')
