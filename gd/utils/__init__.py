# -*- encoding: utf-8 -*-
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
"""This module holds general useful functions that are too generic to be
placed anywhere else.
"""

import string
import random
import smtplib
import re

from email.mime.text import MIMEText
from json import dumps as internal_dumps
from datetime import date, datetime
from StringIO import StringIO
from PIL import Image, ImageOps
from gettext import gettext
from flask import url_for
# from twython import Twython
import tweepy
import pdb
import sys
import traceback
from gd.utils.gdcache import fromcache, tocache

from gd import conf
from datetime import datetime, timedelta
from email.utils import parsedate_tz

def _default_handler(value):
    """Handles usually unserializable objects, currently datetime and
    date objects, converting them to an isoformatted string
    """
    if isinstance(value, (date, datetime)):
        return datetime.isoformat(value)


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata
    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)


def convert_todatetime(s=None):

    # s = 'Tue Mar 29 08:11:25 +0000 2011'
    if not s:
        return None

    time_tuple = parsedate_tz(s.strip())
    dt = datetime(*time_tuple[:6])
    # return dt - timedelta(seconds=time_tuple[-1])
    return dt

def get_twitter_connection():
    auth = tweepy.OAuthHandler(conf.TWITTER_CONSUMER_KEY, conf.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(conf.TWITTER_ACCESS_TOKEN, conf.TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def twitts(hashtag=None, count=25):
    print "->>twitts desabilitada!"
    return []

    # result = None
    # if not hashtag:
    #     result = fromcache("twetts_cabecalho")
    # if not result:
    #     t = get_twitter_connection()
    #     if not hashtag:
    #         hashtag = conf.TWITTER_HASH_CABECALHO
    #     result = t.search(hashtag, result_type='mixed', count=count)
    #     # pdb.set_trace()
    #     # tws = [status for status in result['statuses']]
    #     result = []
    #     for status in result:
    #         # print status
    #         status['classe'] = 'pessoa' + str(random.choice(range(1,10)))
    #         status['created_at'] = convert_todatetime(status.created_at)
    #         result.append(status)

    #     tocache("twetts_cabecalho", result)
    # # print result
    # # print len(result)
    # return result


def dumps(obj):
    """Replacement for builtin `json.dumps' that handles usual
    unserializable objects, like `datetime' instances.
    """
    return internal_dumps(obj, default=_default_handler)


def nts(string):
    """Ensures that a string will not end with a trailing slash"""
    if string.endswith('/'):
        return string[:-1]
    return string


LINK_RE = re.compile('(https?\:\/\/[(\w|\d|+|-|_|\.|\/)]+)')
def replinks(string, target="_blank"):
    """Find urls and replace them with an html link"""
    return LINK_RE.sub(
        '<a target="%s" href="\g<0>">\g<0></a>' % target,
        string)


# -- JSON Messages --


class msg(object):
    """Namespace to hold message stuff"""

    @staticmethod
    def ok(data):
        """Ok message"""
        return dumps({ 'status': 'ok', 'msg': data })

    @staticmethod
    def error(data, code=None):
        """Error message"""
        ret = { 'status': 'error', 'msg': data }
        if code is not None:
            ret.update({ 'code': code })
        return dumps(ret)


# -- Image manipulation --


def thumbnail(data, size, fit=True):
    """Generates a thumbnail for an image `data'"""
    output = StringIO()
    img = Image.open(data)
    if fit: # Means that we'll have to respect the size
        img = ImageOps.fit(img, size, Image.ANTIALIAS)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(output, 'PNG')
    output.seek(0)
    return output



# -- Form handling --

def format_csrf_error(form, orig, code):
    """This function wraps an error message and, instead of
    returning the data content, it adds the a new field: a new csrf
    token.

    It's safe to do it here because only people that sent a valid
    csrf token in the first time can get a new one.
    """
    data = { 'data': orig }
    if 'csrf' in dir(form):
        data.update({ 'csrf': form.csrf.data })
    return msg.error(data, code)


# -- E-mail password

def generate_random_password():
    """As the name says, this method generates random passwords"""
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(8))


def sendmail(subject="", to_addr="", message=""):
    """Sends an email message"""
    try:
        msg = MIMEText(message, _charset='utf-8')

        # Setting message headers
        msg['Subject'] = subject
        msg['To'] = to_addr
        msg['From'] = conf.FROM_ADDR

        # Finally, sending the mail
        smtp = smtplib.SMTP(conf.SMTP)
        smtp.sendmail(conf.FROM_ADDR, to_addr, msg.as_string())
        smtp.quit()
    except Exception as e:
        print "Ocorreu um erro enviando email para %s" % to_addr
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    return True


def send_password(addr, password):
    """Sends a new password to an user that forgot his/her choosen
    one"""
    # Setting the message body
    return sendmail(
        conf.PASSWORD_REMAINDER_SUBJECT, addr,
        conf.PASSWORD_REMAINDER_MSG % {
            'password': password,
            'siteurl': conf.BASE_URL,
        }
    )


def send_welcome_email(user):
    """Sends a welcome message to brand new users"""
    # Setting the message body
    url = url_for('confirm_signup', key=user.user_activation_key)
    return sendmail(
        conf.WELCOME_SUBJECT, user.email,
        conf.WELCOME_MSG % {
            'username': unicode(user.display_name),
            'siteurl': conf.BASE_URL,
            'confirmation_url': url[1:],
        }
    )

def categoria_contribuicao_text(id):
    """Retorna a descricao do item conforme o ID recebido"""
    return [
        '',
        u'Entidades de classe dos profissionais da comunicação social',
        u'Empresas de comunicação e instituições representativas do setor',
        u'Entidades ligadas à comunicação comunitária',
        u'Instituições da sociedade civil e movimentos sociais',
        u'Instituições de ensino e pesquisa da área da comunicação social no Rio Grande do Sul',
    ][int(id)];


def gen_getkey(chave):
    def getkey(x):
        try:
            return int(x[chave])
        except ValueError:
            return x[chave]
    return getkey

def treat_categories(videos, unico=False, orderby=None):
    #Como a lista de videos vem com as várias categorias, o resultado da query
    #traz videos duplicados na lista, então este método une em 1 item apenas
    #o mesmo vídeo com suas várias catetorias
    todos = {}

    if unico:
        videos = [videos]

    print videos

    for video in videos:
        # print "XX Video:", video['id'], video['views']
        if video['category']:
            if video['id'] in todos.keys():
                todos[video['id']]['category'] = todos[video['id']]['category'] + "," + video['category']
            else:
                todos[video['id']] = video
                todos[video['id']]['category_list'] = []

            todos[video['id']]['category_list'].append( {'id':video['category'], 'name':video['category_name']})
        else:
            todos[video['id']] = video

    if orderby:
        if "desc" in orderby.lower():
            rev = True
            orderby = orderby.split(' ')[0]
        else:
            rev = False
        lista = todos.values()
        lista.sort(key=gen_getkey(orderby) , reverse=rev)
        retorno = lista
    else:
        retorno = todos.values()

    if unico:
        return retorno[0]
    else:
        return retorno

    # if unico:
    #     return todos.values()[0]
    # else:
    #     return todos.values()
