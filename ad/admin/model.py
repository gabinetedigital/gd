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

from elixir import *
from datetime import datetime
import os


class StreamingChannel(Entity):
    using_options(shortnames=True)

    source = Field(Unicode(150))
    format = Field(Unicode(200))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode)
    audience = ManyToOne('Audience')

    def __str__(self):
        return '<StreamingChannel "%s">' % self.source

class Term(Entity):
    using_options(shortnames=True)

    hashtag = Field(Unicode(45))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode)
    audience = ManyToOne('Audience')

    def __str__(self):
        return '<Term "%s">' % self.hashtag

class Audience(Entity):
    using_options(shortnames=True)

    title = Field(Unicode(250))
    description = Field(UnicodeText)
    date = Field(DateTime)
    creation_date = Field(DateTime, default=datetime.now)
    terms = OneToMany('Term')
    visible = Field(Boolean, default=True)
    owner = Field(Unicode)
    #themes = ManyToOne('Theme')
    sources = OneToMany('StreamingChannel')

    def __str__(self):
        return '<Audience "%s" (%d)>' % (self.description, self.date)


# class Theme(Entity):
#     using_options(shortnames=True)

#     name = Field(Unicode)
#     creation_date = Field(DateTime, default=datetime.now)
#     creator = Field(Unicode)
#     audience = OneToMany('Audience', inverse='themes')

#     def __str__(self):
#         return '<Theme "%s">' % self.name


#metadata.bind = "sqlite:///db"
metadata.bind = "sqlite:///%s" % os.path.join(os.path.dirname(__file__), "db")
metadata.bind.echo = True
setup_all(__name__ == '__main__')
