#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013  Governo do Estado do Rio Grande do Sul
#
#   Author: Guilherme Guerra de Almeida <guerrinha@comum.org>
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
from flask import Blueprint, request, render_template, abort, current_app, Response, url_for, jsonify
from werkzeug import secure_filename
from jinja2.utils import Markup

import os
import re
import xmlrpclib
import traceback
from hashlib import md5

# from gd.auth import is_authenticated, authenticated_user #, NobodyHome
from gd import auth as authapi
from gd.utils import dumps, sendmail, send_welcome_email, twitts
from gd.model import UserFollow, session as dbsession
from gd.content import wordpress
from gd.utils.gdcache import fromcache, tocache #, cache, removecache
from gd.utils import twitts
from gd import conf

from instagram.client import InstagramAPI
import flickrapi

seminario = Blueprint(
    'seminario', __name__,
    template_folder='templates',
    static_folder='static')



def get_instagram_photos():

    # É necessário configurar os campos INSTAGRAM_TOKEN e INSTAGRAM_USER
    # no conf.py

    try:
        access_token = conf.INSTAGRAM_TOKEN
    except KeyError:
        access_token = ""

    try:
        user_id = conf.INSTAGRAM_USER
    except KeyError:
        user_id = ""

    search_tag = conf.SEMINARIO_INSTAGRAM_TAG

    api = InstagramAPI(access_token=access_token)
    # recent_media, next = api.user_recent_media(user_id=user_id, count=-1)
    recent_media, next = api.tag_recent_media(tag_name=search_tag, count=20)
    print recent_media
    photos = []
    for media in recent_media:
        # if hasattr(media, 'tags'):
            # if tag in [ t.name for t in media.tags ]:
        print media, dir(media)
        content = { 'link': media.link,
                    'url': media.images['standard_resolution'].url,
                    'thumb': media.images['thumbnail'].url,
                    'caption': media.caption.text if media.caption else "",
                    'tags': media.tags }
        photos.append(content)

    return photos



def get_flickr_photos():

    api_key = conf.FLICKR_APP_KEY
    api_secret = conf.FLICKR_APP_SECRET

    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=False)
    
    photos = flickr.photos_search(tags=conf.SEMINARIO_FLICKR_TAG, per_page='10')
    print "PROCURANDO POR", conf.SEMINARIO_FLICKR_TAG, "NO FLICKR"
    
    retorno = []
    # print "FLICKR \/"
    # print photos
    # print photos[0]
    for photo in photos[0]:
        obj = {}
        # print "  ", photo.get('id'), photo.keys()
        obj['id'] = photo.get('id')
        obj['title'] = photo.get('title')
        obj['owner'] = photo.get('owner')
        # infos = flickr.photos_getInfo(photo_id=photo.get('id'))
        sizes = flickr.photos_getSizes(photo_id=photo.get('id'))
        # print "    x", sizes.keys()
        for size in sizes:
            # img = size[0]
            for img in size:
                print "      ", img.get('source'), img.get('label') #, img.keys()
                obj[img.get('label')] = img.get('source')
        retorno.append(obj)
    # print retorno
    # print "FLICKR /\\"
    return retorno

@seminario.route('/')
def index():
    return render_template('seminario.html')


@seminario.route('/cobertura/')
def cobertura():
    twitter_tag = conf.SEMINARIO_TWITTER_TAG
    cid = conf.SEMINARIO_CATEGORIA_ID
    pagination, posts = fromcache("seminario_posts") or tocache("seminario_posts", wordpress.getPostsByCategory(cat=cid))
    twites = fromcache("seminario_twitts") or tocache("seminario_twitts", twitts(hashtag=twitter_tag, count=5) )
    photos = get_flickr_photos()
    instaphotos = get_instagram_photos()
    # print posts
    # print twites

    return render_template('cobertura.html', posts=posts, twitts=twites, photos=photos, instaphotos=instaphotos)

@seminario.route('/newlink/', methods=['POST'])
def newlink():
    return jsonify({'status':0, 'msg':'Obrigado pela sua contribuição!'})