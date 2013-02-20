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
    url_for, abort, current_app

from gd.model import Audience, Term, get_or_404, AudiencePosts
from gd.utils import dumps
from gd import conf

from gd.content.wp import wordpress

# Instagram API
from instagram.client import InstagramAPI

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
    print "POSTS====================="
    print posts
    how_to = wordpress.getPageByPath('how-to-use-governo-escuta')

    return render_template(
        'govescuta.html',
        menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal'),
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
    tag = None
    for cat in inst:
        category = cat['category']
        tag = cat['category_slug']

    if category:
        pagination, posts = wordpress.getPostsByCategory(
            cat=category)
    else:
        pagination, posts = None, []

    try:
        access_token = current_app.config['INSTAGRAM_TOKEN']
    except KeyError:
        access_token = ""

    api = InstagramAPI(access_token=access_token)
    recent_media, next = api.user_recent_media(user_id="227330958")
    photos = []
    for media in recent_media:
        if hasattr(media, 'tags'):
            if tag in [ t.name for t in media.tags ]:
                content = { 'url': media.images['standard_resolution'].url,
                            'thumb': media.images['thumbnail'].url,
                            'caption': media.caption.text }
                photos.append(content)


    buzzes = AudiencePosts.query.get(aid).get_moderated_buzz()
    buzzesSelec = AudiencePosts.query.get(aid).get_last_published_notice()
    govescuta = True
    video_sources = {}
    audience = inst[0]
    if audience['video_sources']:
        for s in audience['video_sources']:
            if(s['format'].find(';') > 0):
                f = s['format'][0:s['format'].find(';')]
            else:
                f = s['format']
            video_sources[f] = s['url']
    return render_template(
        'audience.html', #this template is from gd/audience
        # 'govescuta_edicaoanter.html',
        sources=video_sources,
        audiences=inst,
        referrals=posts,
        pagination=pagination,
        buzzes = buzzes,
        buzzesSelec = buzzesSelec,
        menu=menus,
        tag=tag,
        govescuta=govescuta,
        photos=photos,
        how_to=getattr(how_to, 'content', ''),
    )
