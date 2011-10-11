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

"""Module that defines all models used in our app.

All entity mappers are defined using the `Elixir' API and some signals
are sent using the `sio' module.
"""

from hashlib import md5
from datetime import datetime
from sqlalchemy import not_, desc, event
from elixir.events import after_insert, before_insert
from elixir import using_options, setup_all, metadata, session
from elixir import Entity, Field, Unicode, UnicodeText, DateTime, \
    Boolean, Integer, Enum, ManyToOne, OneToMany

from ad import conf
from ad.buzz import sio
from ad.utils import phpass

class Term(Entity):
    """Mapper for the `term' entity
    """
    using_options(shortnames=True)

    hashtag = Field(Unicode(45))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode(64))
    main = Field(Boolean)
    audience = ManyToOne('Audience')

    def __str__(self):
        return self.hashtag

class Audience(Entity):
    """Mapper for the `audience' entity
    """
    using_options(shortnames=True)

    title = Field(Unicode(256))
    subject = Field(UnicodeText)
    description = Field(UnicodeText)
    date = Field(DateTime)
    creation_date = Field(DateTime, default=datetime.now)
    terms = OneToMany('Term')
    visible = Field(Boolean, default=True)
    live = Field(Boolean, default=True)
    owner = Field(Unicode(64))
    embed = Field(Unicode(256))
    buzzes = OneToMany('Buzz')

    def __str__(self):
        return '<%s "%s" (%d)>' % (
            self.__class__.__name__, self.description, self.date)

    @after_insert
    def notify(self):
        """Notify our buzz system that we have a new audience"""
        sio.send('new_audience', { 'id': self.id })

    def get_main_term(self):
        """Returns the main term of the current audience"""
        return Term.query.filter_by(main=1, audience=self).one().hashtag

    def get_public_buzz(self):
        """Returns the public notice buzz"""
        return Buzz.query \
            .filter_by(audience=self) \
            .order_by(desc('creation_date')) \
            .all()

    def get_moderated_buzz(self):
        """Returns the moderated notice buzz"""
        return Buzz.query \
            .filter_by(audience=self) \
            .filter(not_(Buzz.status.in_(['inserted']))) \
            .order_by(desc('creation_date')) \
            .all()


class Buzz(Entity):
    """Mapper for the `buzz' entity
    """
    using_options(shortnames=True)

    owner_nick = Field(Unicode(64))
    owner_email = Field(Unicode(128))
    owner_avatar = Field(Unicode(256))
    content = Field(Unicode(512))
    status = Field(Enum(u'inserted', u'approved', u'selected', u'published'),
                   default=u'inserted')
    creation_date = Field(DateTime, default=datetime.now)
    audience = ManyToOne('Audience')
    type_ = ManyToOne('BuzzType')

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.content)

    def to_dict(self, deep=None):
        """Just a shortcut for `super.to_dict' passing the `type_' field
        to the `deep' attribute by default.
        """
        if deep is None:
            deep = { 'type_': {} }
        return super(Buzz, self).to_dict(deep=deep)

    @after_insert
    def notify(self):
        """Notify our buzz system that we have a new audience"""
        sio.send('new_buzz', self.to_dict())


class BuzzType(Entity):
    """Mapper for the `buzztype' entity
    """
    using_options(shortnames=True)

    name = Field(Unicode(64))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode(64))
    buzzes = OneToMany('Buzz')

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.name)


class UserMeta(Entity):
    """Mapper for the wp_usermeta entity, the same used by wordpress"""
    using_options(tablename='wp_usermeta')

    umeta_id = Field(Integer, primary_key=True)
    user_id = Field(Integer)
    meta_key = Field(Unicode(256))
    meta_value = Field(UnicodeText)


class User(Entity):
    """Mapper for the `user' entity that is the same table used by
    wordpress"""
    using_options(tablename='wp_users')

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(64), colname='user_nicename')
    nickname = Field(Unicode(64), colname='display_name')
    username = Field(Unicode(64), colname='user_login')
    password = Field(Unicode(256), colname='user_pass')
    email = Field(Unicode(64), colname='user_email')
    creation_date = Field(
        DateTime, colname='user_registered',
        default=datetime.now)
    status = Field(
        Boolean, colname='user_status',
        default=True)
    url = Field(
        Unicode(256),
        colname='user_url',
        default=u'')

    @before_insert
    def set_defaults(self):
        """Sets default values to fields that depends on other field
        values to be set before inserting"""
        if not self.name:
            self.name = unicode(self.username)
        if not self.nickname:
            self.nickname = unicode(self.name)

    @before_insert
    def hash_password(self):
        """Converts the password field into an md5 hashed string"""
        hasher = phpass.PasswordHash(8, False)
        self.password = hasher.hash_password(self.password)

    def public_dict(self):
        """Returns all public items about the user in a dict format"""
        # It's easier to create a new dict than selecting each public
        # field from the `.to_dict()' return.
        return dict(
            id=self.id,
            name=self.name,
            nickname=self.nickname,
            username=self.username,
            creation_date=self.creation_date,
            url=self.url,
        )


@event.listens_for(session, "after_flush")
def _set_user_meta(session, flush_context):
    """Sets all meta information needed by wordpress, such as
    nickname and capabilities"""
    if not session.is_active:
        # Let's do nothing if the session is not ready
        return
    for inst in session.new:
        if not isinstance(inst, User):
            # We're not interested in anything different from a new user
            continue
        UserMeta(
            user_id=inst.id, meta_key=u'nickname',
            meta_value=inst.username)
        UserMeta(
            user_id=inst.id, meta_key=u'wp_capabilities',
            meta_value=u'a:1:{s:10:"subscriber";s:1:"1";}')
        UserMeta(
            user_id=inst.id, meta_key=u'wp_user_level',
            meta_value=u'0')


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
        for key, val in kwargs.iteritems():
            params[key] = val
        instance = model(**params)
        session.add(instance)
        return instance, True


# Database setup

metadata.bind = conf.DATABASE_URI
metadata.bind.echo = True
setup_all(__name__ == '__main__')
