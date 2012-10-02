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

from gd.model import Audience, Term, get_or_404, AudiencePosts
from gd.utils import dumps

from gd.content.wp import wordpress

govescuta = Blueprint(
    'govescuta', __name__,
    template_folder='templates',
    static_folder='static')


@govescuta.route('/')
def index(page=0):
    sortby = request.values.get('sortby') or 'date'
    pagination, posts = wordpress.wpgove.getAudiencias(
                                            page=page,
                                            sortby=sortby,
                                            totalporpage='10')

    how_to = wordpress.getPageByPath('how-to-use-governo-escuta')

    return render_template(
        'govescuta.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        audiences=posts,
        sortby=sortby,
        how_to=getattr(how_to, 'content', ''),)

@govescuta.route('/<int:aid>')
def govescuta_details(aid):
    """Renders an audience with its public template"""
    pagination, inst = wordpress.wpgove.getAudiencias(postID=aid)
    how_to = wordpress.getPageByPath('how-to-use-governo-escuta')
    menus = wordpress.exapi.getMenuItens(menu_slug='menu-principal')
    category = None
    for cat in inst:
        category = cat['category']

    if category:
        pagination, posts = wordpress.getPostsByCategory(
            cat=category)
    else:
        pagination, posts = None, []

    print inst
    buzzes = AudiencePosts.query.get(aid).get_moderated_buzz()
    buzzesSelec = AudiencePosts.query.get(aid).get_last_published_notice()
    return render_template(
        'audience.html', #this template is from gd/audience
        # 'govescuta_edicaoanter.html',
        audiences=inst,
        referrals=posts,
        pagination=pagination,
        buzzes = buzzes,
        buzzesSelec = buzzesSelec,
        menu=menus,
        how_to=getattr(how_to, 'content', ''),
    )

