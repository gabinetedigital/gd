#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Sergio Berlotto <sergio.berlotto@gmail.com>
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

import locale
from flask import Blueprint, request, render_template, abort, current_app, Response, url_for
from werkzeug import secure_filename
from jinja2.utils import Markup
# import numpy as np

# import datetime as d
# import os
# import re
# import xmlrpclib
# import traceback
# import random
# import string
# import pdb
# from hashlib import md5

# from gd.auth import is_authenticated, authenticated_user #, NobodyHome
# from gd import auth as authapi
# from gd.utils import dumps, sendmail, send_welcome_email, send_password, twitts, get_twitter_connection, treat_categories
# from gd.model import UserFollow, session as dbsession
# from gd.content.wp import wordpress
# from gd.utils.gdcache import fromcache, tocache, cache, removecache
# from gd import conf

resultados = Blueprint(
    'resultados', __name__,
    template_folder='templates',
    static_folder='static')


@resultados.route('/')
def index_resultados():
	return render_template('resultados_index.html')