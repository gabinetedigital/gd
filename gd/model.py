# -*- encoding: utf-8 -*-
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

import locale

from datetime import datetime
from elixir import Entity, Field, Unicode, UnicodeText, DateTime, Boolean, \
    Integer, Enum, ManyToOne, OneToMany, ManyToMany, String, Text, using_options, \
    setup_all, metadata, session
import elixir
from elixir.events import after_insert, before_insert
from flask import url_for, abort
from flaskext.uploads import UploadConfiguration, UploadSet, IMAGES
from gd import conf
from gd.utils import phpass, dumps
from sqlalchemy import not_, desc, event, create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker(autoflush=True))
# elixir.scoped_session = Session
scoped_session = Session

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')


def _configuploadset(name, constraint):
    uset = UploadSet(name, constraint)
    uset._config = UploadConfiguration(
        conf.UPLOADS_DEFAULT_DEST,
        conf.UPLOADED_FILES_URL,
    )
    return uset



class MayorTweet(Entity):
    """Mapper for the `governor_last_tweet' entity
    """
    using_options(shortnames=True)
    text = Field(Unicode(140))

    @staticmethod
    def save_tweet(text):
        gt = MayorTweet.get_current()
        if gt is None:
            gt = MayorTweet()

        # Making sure we'll not save anything but unicode text.
        gt.text = unicode(text)
        session.commit()

    @staticmethod
    def get_current():
        return MayorTweet.query.get(1)

class Upload(object):
    imageset = _configuploadset('images', IMAGES + ('',))


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

class AudiencePosts(Entity):
    """Mapper for the wp_usermeta entity, the same used by wordpress"""
    using_options(tablename='wp_posts')

    id = Field(Integer, primary_key=True, colname='ID')
    audience = OneToMany('AudiencePostsMeta')

    def __str__(self):
        return '<%s "%s">' % (
            self.__class__.__name__, self.id)

    def get_moderated_buzz(self, offset=0, limit=-1, except_ids=[]):
        """Returns the moderated notice buzz"""
        except_ids = except_ids or [-1]
        return Buzz.query \
            .filter_by(audience_id=self.id) \
            .filter(Buzz.status.in_(['approved', 'selected'])) \
            .filter(not_(Buzz.id.in_(except_ids))) \
            .order_by(desc('creation_date')) \
            .all()

    def get_public_buzz(self, offset=0, limit=-1, except_ids=[]):
        """Returns the public notice buzz"""
        except_ids = except_ids or [-1]
        query = Buzz.query \
            .filter_by(audience_id=self.id) \
            .filter(Buzz.status.in_(['inserted'])) \
            .filter(not_(Buzz.id.in_(except_ids))) \
            .order_by(desc('creation_date'))
        return limit > 0 and query[offset:limit] or query.all()

    def get_selected_buzz(self, except_ids=[]):
        """Returns the selected notice buzz"""
        except_ids = except_ids or [-1]
        return Buzz.query \
            .filter_by(audience_id=self.id) \
            .filter(Buzz.status.in_(['selected'])) \
            .filter(not_(Buzz.id.in_(except_ids))) \
            .order_by(desc('creation_date')) \
            .all()

    def get_last_published_notice(self):
        """Returns the last published notice about this audience"""
        try:
            return Buzz.query \
                .filter_by(audience_id=self.id, status=u'published') \
                .order_by(desc('date_published')) \
                .first()
        except NoResultFound:
            return None

    def get_all_buzz(self):
        """Returns the selected notice buzz"""
        return Buzz.query \
            .filter_by(audience_id=self.id) \
            .order_by(desc('creation_date')) \
            .all()

class AudiencePostsMeta(Entity):
    """Mapper for the wp_usermeta entity, the same used by wordpress"""
    using_options(tablename='wp_postmeta')

    meta_id = Field(Integer, primary_key=True)
    post = ManyToOne('AudiencePosts')
    meta_key = Field(Unicode(256))
    meta_value = Field(UnicodeText)

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.content)

class Audience(Entity):
    """Mapper for the `audience' entity
    """
    using_options(shortnames=True)

    #msgid = Field(id)
    id = Field(Integer, primary_key=True)
    title = Field(Unicode(256))
    subject = Field(UnicodeText)
    description = Field(UnicodeText)
    date = Field(DateTime)
    creation_date = Field(DateTime, default=datetime.now)
    terms = OneToMany('Term')
    visible = Field(Boolean, default=False)
    started = Field(Boolean, default=False)
    date_started = Field(DateTime)
    owner = Field(Unicode(64))
    embed = Field(Unicode(256))
    #buzzes = OneToMany('Buzz')

    def __str__(self):
        return '<%s "%s" (%d)>' % (
            self.__class__.__name__, self.description, self.date)

    def get_main_term(self):
        """Returns the main term of the current audience"""
        return Term.query.filter_by(main=1, audience=self).one().hashtag


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
    date_published = Field(DateTime)
    creation_date = Field(DateTime, default=datetime.now)
    audience_id = Field(Integer)
    type_ = ManyToOne('BuzzType')
    user = ManyToOne('User')

    face_msg_id = Field(Unicode(50), unique=True)
    """
    ALTER TABLE `buzz` ADD COLUMN `face_msg_id` VARCHAR(50) NULL
    , ADD UNIQUE INDEX `face_msg_id_UNIQUE` (`face_msg_id` ASC) ;
    """

    def __str__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.content)

    def to_dict(self, deep=None):
        """Just a shortcut for `super.to_dict' passing the `type_' field
        to the `deep' attribute by default.
        """
        if deep is None:
            deep = { 'type_': {}, 'user': {} }
        base = super(Buzz, self).to_dict(deep=deep)
        base['avatar'] = self.avatar
        if base['user'] and self.user:
            base['user'] = self.user.public_dict()
        return base

    @property
    def avatar(self):
        """Returns the avatar of the user that posted a notice"""
        return self.owner_avatar or self.user.avatar_url


class BuzzType(Entity):
    """Mapper for the `buzztype' entity
    """
    using_options(shortnames=True)

    name = Field(Unicode(64))
    creation_date = Field(DateTime, default=datetime.now)
    creator = Field(Unicode(64))
    buzzes = OneToMany('Buzz')

    def __str__(self):
        return self.name


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
    user_activation_key = Field(Unicode(60))

    receive_sms   = Field(Boolean)
    receive_email = Field(Boolean)

    buzzes = OneToMany('Buzz')
    contribs = OneToMany('Contrib')
    follows = OneToMany('UserFollow')
    creation_date = Field(
        DateTime, colname='user_registered',
        default=datetime.now)
    status = Field(
        Boolean, colname='user_status',
        default=True)

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
        """Converts the password field into a phpass hashed string"""
        print "\n\nGRAVANDO SENHA NOVA 1:",self.password
        hasher = phpass.PasswordHash(8, False)
        self.password = hasher.hash_password(self.password)
        print "GRAVANDO SENHA NOVA 2:",self.password,"\n\n"

    def set_password(self, passwd):
        """Updates the user's password

        This method does _not_ update the database itself, please call
        the '''session.commit()''' method.
        """
        self.password = passwd
        self.hash_password()

    def has_roles(self, roles):
        """Returns True if the current user has one of the given roles.

        This method uses the `OR' logic. If the user has _AT LEAST ONE_
        of the specified roles, it'll return True.
        """

        # Making sure we're handling lists or tuples
        if not isinstance(roles, (list, tuple)):
            raise TypeError('has_roles() does not handle any thing but '
                            'lists and tuples')

        # So, let's query for the usermeta object. Once we don't handle
        # wordpress registered rows, let's make sure that it will never
        # raise an unexpected exception.
        query = UserMeta.query.filter_by(
            user_id=self.id,
            meta_key='wp_capabilities')
        try:
            meta = query.one()
        except NoResultFound:
            return False

        # Now it is tome to make sure that the user has _AT LEAST ONE_
        # of the roles specified in the `roles' param.
        return True in [i.lower() in meta.meta_value for i in roles]

    def public_dict(self):
        """Returns all public items about the user in a dict format"""
        # It's easier to create a new dict than selecting each public
        # field from the `.to_dict()' return.
        return dict(
            id=self.id,
            name=self.name,
            nickname=self.nickname,
            email=self.email,
            display_name=self.display_name,
            avatar_url=self.avatar_url,
            creation_date=self.creation_date,
            facebook=self.get_meta('facebook'),
            twitter=self.get_meta('twitter')
        )

    def public_json(self):
        """Returns the same content as `public_dict()', but in JSON
        format"""
        return dumps(self.public_dict())

    @property
    def avatar_url(self):
        """Returns the avatar image of this user or the default one"""
        fname = self.get_meta('avatar')
        return fname and Upload.imageset.url(fname) or \
            url_for('static', filename='img/avatar.png')

    @property
    def display_name(self):
        """Just a shortcut to decide which value should be exposed to
        identify a user"""
        return self.nickname or self.name

    def get_meta(self, key):
        """Returns a value of a meta var of a user"""
        try:
            return UserMeta.query \
                .filter_by(user_id=self.id, meta_key=key) \
                .one() \
                .meta_value
        except NoResultFound:
            return None

    def set_meta(self, key, value):
        """Set a meta value for the user instance.

        This method does not flush to the database! So you have to call
        the `session.commit()' method after calling it."""
        meta = get_or_create(UserMeta, user_id=self.id, meta_key=key)[0]
        meta.meta_value = value

    def metadata(self):
        """Returns _all_ metadata set for an user instance.

        This method is here to clean a mess created by using the
        wordpress scheme. Because of this choice, we have user metadata
        split between the `wp_users' and `wp_user_meta' tables (and,
        sometimes, coming from a social network).

        So, to fix this situation, I've at least wrote this method to
        provide an encapsulated method to get all metadata associated
        with an user instance.

        Be careful exposing this method to the end users. It will return
        all the information about an user, including his/her (hashed)
        password string, mail address, etc.
        """
        data = self.to_dict()
        data.update(dict((i.meta_key, i.meta_value) for i in
                     UserMeta.query.filter_by(user_id=self.id).all()))
        return data


class Contrib(Entity):
    """Mapper for the `contrib' entity
    """
    using_options(shortnames=True)

    title = Field(String(256))
    content = Field(String(600))
    original = Field(String(600), default='')
    status = Field(Boolean, default=False)
    enabled = Field(Boolean, default=True)
    parent = Field(Integer, default=0)
    moderation = Field(Boolean, default=False)
    user = ManyToOne('User')
    creation_date = Field(DateTime, default=datetime.now)
    children = ManyToMany('Contrib')
    theme = Field(Enum(
        u'cuidado', u'familia', u'emergencia',
        u'medicamentos', u'regional'
    ))


class ComiteNews(Entity):
    """Mapper for the `comite` news, sent by users"""
    using_options(tablename='comite_news')
    user = ManyToOne('User')
    creation_date = Field(DateTime, default=datetime.now)
    title = Field(String(500,convert_unicode=True))
    content = Field(Text(convert_unicode=True))

class CadastroComite(Entity):
    """Cadastro de dados para participar do comite de transito"""
    using_options(tablename='cadastro_comite')
    nome = Field(String(500,convert_unicode=True))
    email = Field(String(500,convert_unicode=True))
    telefone = Field(String(500,convert_unicode=True))
    cidade = Field(String(500,convert_unicode=True))
    creation_date = Field(DateTime, default=datetime.now)


class UserFollow(Entity):
    """Controle dos usuários que seguem as obras do monitoramento"""
    using_options(tablename='user_follow')

    # id = Field(Integer, primary_key=True)
    user = ManyToOne('User')
    obra_id = Field(Integer)
    mode = Field(String(15,convert_unicode=True))
    datetime = Field(DateTime, default=datetime.now)
    facebook_id = Field(String(500,convert_unicode=True))
    twitter_id  = Field(String(500,convert_unicode=True))
    email       = Field(String(500,convert_unicode=True))

class VotosReforma(Entity):
    """Dados da votacao sobre a reforma politica"""
    using_options(tablename='votos_reforma')
    opcao1 = Field(Integer)
    opcao2 = Field(Integer)


class LinkColaborativo(Entity):
    """Links enviados pelos jornalistas no Seminário da Crise"""
    using_options(tablename='link_colaborativo')
    nome     = Field(String(100))
    email    = Field(String(500))
    link     = Field(String(700))
    site     = Field(String(100))
    clicks   = Field(Integer)
    imagem   = Field(String(700))
    datetime = Field(DateTime, default=datetime.now)


class InscricaoSeminario(Entity):
    using_options(tablename='inscricao_seminario')
    nome     = Field(String(100))
    email    = Field(String(500))
    telefone = Field(String(30))
    twitter  = Field(String(100))
    facebook = Field(String(100))
    site     = Field(String(500))
    colaborativa = Field(Boolean)
    colaborativa_modo = Field(String(200))
    datetime = Field(DateTime, default=datetime.now)


class HistoricoSeminario(Entity):
    using_options(tablename='historico_seminario')
    item_id  = Field(String(500))
    objeto   = Field(String(100))
    url      = Field(String(700))
    user_id  = Field(String(500))
    texto    = Field(String(500))
    datetime = Field(DateTime, default=datetime.now)


@event.listens_for(session, "after_flush")
def _set_user_meta(lsession, flush_context):
    """Sets all meta information needed by wordpress, such as
    nickname and capabilities"""
    if not lsession.is_active:
        # Let's do nothing if the session is not ready
        return
    for inst in lsession.new:
        if not isinstance(inst, User):
            # We're not interested in anything different from a new user
            continue
        inst.set_meta(u'nickname', inst.name or inst.username)
        inst.set_meta(u'wp_capabilities', u'a:1:{s:10:"subscriber";s:1:"1";}')
        inst.set_meta(u'wp_user_level', u'0')


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


def get_or_404(model, **kwargs):
    """Similar to the get_or_404 Django shortcut.

    Returns an instance of a given model that can be found with `kwargs'
    filter params or calls the `abort' function with a 404 error.
    """
    try:
        return model.query.filter_by(**kwargs).one()
    except NoResultFound:
        abort(404)


# Database setup

metadata.bind = create_engine(conf.DATABASE_URI, pool_recycle=1800, pool_size=15, echo=conf.DEBUG)
# metadata.bind = conf.DATABASE_URI
# metadata.bind.echo = conf.DEBUG
setup_all(__name__ == '__main__')


if __name__ == '__main__':
    import sys
    import os
    if len(sys.argv) > 2:
        User(
            username=unicode(sys.argv[1]),
            password=unicode(sys.argv[2]),
            email=os.getenv('EMAIL') or sys.argv[3])
        session.commit()
