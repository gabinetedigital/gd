# -*- coding:utf-8 -*-
#
# Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
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

from flask import Blueprint, render_template, abort
from gd.content.wp import wordpress, gallery as api

gallery = Blueprint(
    'gallery', __name__,
    template_folder='templates',
    static_folder='static')


@gallery.route('/')
@gallery.route('/<int:gid>')
def index(gid=None):
    galleries = wordpress.wpgd.getGalleries()
    if not galleries:
        abort(404)
    if gid and (str(gid) not in [i['gid'] for i in galleries]):
        abort(404)
    current = wordpress.wpgd.getGallery(gid or galleries[0]['gid'])
    return render_template(
        'gallery.html',
        galleries=galleries,
        current=current)
