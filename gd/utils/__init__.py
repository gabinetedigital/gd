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

from email.mime.text import MIMEText
from json import dumps as internal_dumps
from datetime import date, datetime
from StringIO import StringIO
from PIL import Image, ImageOps
from gettext import gettext

from gd import conf


def _default_handler(value):
    """Handles usually unserializable objects, currently datetime and
    date objects, converting them to an isoformatted string
    """
    if isinstance(value, (date, datetime)):
        return datetime.isoformat(value)


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
    data.update({ 'csrf': form.csrf.data })
    return msg.error(data, code)


# -- E-mail password

def generate_random_password():
    """As the name says, this method generates random passwords"""
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(8))


def sendmail(subject, to_addr, message):
    """Sends an email message"""
    msg = MIMEText(message, _charset='utf-8')

    # Setting message headers
    msg['Subject'] = subject
    msg['To'] = to_addr
    msg['From'] = conf.FROM_ADDR

    # Finally, sending the mail
    smtp = smtplib.SMTP(conf.SMTP)
    smtp.sendmail(conf.FROM_ADDR, to_addr, msg.as_string())
    smtp.quit()

    print msg.as_string()


def send_password(addr, password):
    """Sends a new password to an user that forgot his/her choosen
    one"""
    # Setting the message body
    sendmail(
        conf.PASSWORD_REMAINDER_SUBJECT, addr,
        conf.PASSWORD_REMAINDER_MSG % {
            'password': password,
            'siteurl': conf.BASE_URL,
        }
    )


def send_welcome_email(user):
    """Sends a welcome message to brand new users"""
    # Setting the message body
    sendmail(
        conf.WELCOME_SUBJECT, user.email,
        conf.WELCOME_MSG % {
            'username': unicode(user.display_name),
            'siteurl': conf.BASE_URL,
        }
    )
