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

from flask import Blueprint, request, render_template, redirect, \
    url_for, abort

from gd.content.wp import wordpress

govescuta = Blueprint(
    'govescuta', __name__,
    template_folder='templates',
    static_folder='static')


@govescuta.route('/')
def index():
    audiences_raw, count = wordpress.gove.getAudiences(
        '',                        # sortby
        '',                        # search
        'audience.visible = true', # filter
        '0',                       # page
    )

    audiences = []
    for audience in audiences_raw[::-1]:
        audience['video'] = wordpress.wpgd.getVideo(audience['data'])
        audiences.append(audience)

    return render_template(
        'govescuta.html',
        audiences=audiences,
        count=count,
    )
