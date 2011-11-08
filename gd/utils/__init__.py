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
from gd import conf

from json import dumps as internal_dumps
from datetime import date, datetime
from StringIO import StringIO
from PIL import Image, ImageOps
import string
import random
from email.mime.text import MIMEText
from gettext import gettext
import smtplib

_ = gettext


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

# -- E-mail password

def generate_random_password():
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(8))


def send_password(to, password):
    print 'sending password to ' + to + '[' + password + ']'

    msg = MIMEText(conf.PASSWORD_REMAINDER_MSG % password)
    msg['Subject'] = conf.PASSWORD_REMAINDER_SUBJECT
    msg['From'] = conf.PASSWORD_REMAINDER_FROM
    msg['To'] = to

    print msg

    print '...sending ...'
    s = smtplib.SMTP(conf.SMTP)
    s.sendmail(conf.PASSWORD_REMAINDER_FROM, to, msg.as_string())
    s.quit()
    print 'sent'
