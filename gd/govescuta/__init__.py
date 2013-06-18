# -*- coding:utf-8 -*-
#
# Copyright (C) 2013  Guilherme Guerra <guerrinha@comum.org>
# Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2012-2013  Governo do Estado do Rio Grande do Sul
#
#   Authors: Lincoln de Sousa <lincoln@gg.rs.gov.br>, Guilherme Guerra
#   <guilherme-guerra@sgg.rs.gov.br>
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

from flask import Blueprint, request, render_template, current_app

from gd.model import AudiencePosts #get_or_404, Audience, Term,
from gd.utils import twitts
from gd import conf
# from json import dumps

from gd.content.wp import wordpress
from gd.utils.gdcache import fromcache, tocache #, removecache

# Instagram API
from instagram.client import InstagramAPI

govescuta = Blueprint(
    'govescuta', __name__,
    template_folder='templates',
    static_folder='static')


@govescuta.route('/')
def index(page=0):
    sortby = request.values.get('sortby') or 'date'
    pagination, posts = fromcache('govescuta-posts-%s' % sortby) or \
                        tocache('govescuta-posts-%s' %sortby,
                                    wordpress.wpgove.getAudiencias(
                                            page=page,
                                            sortby=sortby,
                                            totalporpage='10'))
    how_to = fromcache('howtouse') or tocache('howtouse', wordpress.getPageByPath('how-to-use-governo-escuta'))

    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    try:
        twitter_hash_cabecalho = twitts()
    except:
        twitter_hash_cabecalho = ""

    return render_template(
        'govescuta.html',
        menu=menus,
        # sidebar=wordpress.getSidebar,
        pagination=pagination,
        twitter_hash_cabecalho=twitter_hash_cabecalho,
        audiences=posts,
        sortby=sortby,
        how_to=getattr(how_to, 'content', ''),)

@govescuta.route('/<int:aid>')
def govescuta_details(aid):
    """Renders an audience with its public template"""
    pagination, inst = fromcache('audiencia-escuta-%s' %str(aid)) or \
                       tocache('audiencia-escuta-%s' %str(aid),wordpress.wpgove.getAudiencias(postID=aid))
    how_to = fromcache('how-to-use-governo-escuta') or tocache('how-to-use-governo-escuta', wordpress.getPageByPath('how-to-use-governo-escuta'))
    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    try:
        twitter_hash_cabecalho = twitts()
    except:
        twitter_hash_cabecalho = ""

    category = None
    tag = None
    for cat in inst:
        category = cat['category']
        try:
            tag = cat['category_slug']
        except:
            tag = ""

    if category:
        pagination, posts = fromcache('audiencia-category-%s' % category) or \
                            tocache('audiencia-category-%s' % category,wordpress.getPostsByCategory(
                                       cat=category))
    else:
        pagination, posts = None, []

    try:
        if tag:
            photos = get_instagram_photos(tag)
        else:
            photos = None
    except:
        photos = None

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
        twitter_hash_cabecalho=twitter_hash_cabecalho,
        govescuta=govescuta,
        photos=photos,
        how_to=getattr(how_to, 'content', ''),
    )

@govescuta.route('/instagram_update/<tag>/')
def instagram_update(tag):

    photos = get_instagram_photos(tag)

    return render_template('instagram_update.html', photos=photos)


def get_instagram_photos(tag):

    # É necessário configurar os campos INSTAGRAM_TOKEN e INSTAGRAM_USER
    # no conf.py

    try:
        access_token = current_app.config['INSTAGRAM_TOKEN']
    except KeyError:
        access_token = ""

    try:
        user_id = current_app.config['INSTAGRAM_USER']
    except KeyError:
        user_id = ""

    api = InstagramAPI(access_token=access_token)
    recent_media, next = api.user_recent_media(user_id=user_id, count=-1)
    photos = []
    for media in recent_media:
        if hasattr(media, 'tags'):
            if tag in [ t.name for t in media.tags ]:
                content = { 'url': media.images['standard_resolution'].url,
                            'thumb': media.images['thumbnail'].url,
                            'caption': media.caption.text }
                photos.append(content)

    return photos
