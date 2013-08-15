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
from flask import Blueprint, request, render_template, abort, current_app, Response, url_for, jsonify, make_response
from werkzeug import secure_filename
from jinja2.utils import Markup

import os
import re
import pdb
import xmlrpclib
import traceback
from hashlib import md5

# from gd.auth import is_authenticated, authenticated_user #, NobodyHome
from gd import auth as authapi
from gd.utils import dumps, sendmail, send_welcome_email, twitts
from gd.model import LinkColaborativo, InscricaoSeminario, session as dbsession
from sqlalchemy.exc import IntegrityError
from gd.content import wordpress
from gd.utils.gdcache import fromcache, tocache #, cache, removecache
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

    photos = []

    try:
        api = InstagramAPI(access_token=access_token)
        # recent_media, next = api.user_recent_media(user_id=user_id, count=-1)
        recent_media, next = api.tag_recent_media(tag_name=search_tag, count=20)
        # print recent_media

        for media in recent_media:
            # if hasattr(media, 'tags'):
                # if tag in [ t.name for t in media.tags ]:
            print media, dir(media)
            content = { 'link': media.link,
                        'url': media.images['standard_resolution'].url,
                        'thumb': media.images['low_resolution'].url,
                        'caption': media.caption.text if media.caption else "",
                        'tags': media.tags,
                        'datetime': media.created_time }
            photos.append(content)
    except Exception as e:
        print "ERRO AO BUSCAR AS FOTOS DO INSTAGRAM"
        print e

    return photos



def get_flickr_photos():

    api_key = conf.FLICKR_APP_KEY
    api_secret = conf.FLICKR_APP_SECRET

    flickr = flickrapi.FlickrAPI(api_key, api_secret, cache=False)
    photos = flickr.photos_search(tags=conf.SEMINARIO_FLICKR_TAG, per_page='20')

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
    nome = request.cookies.get('cobertura_nome')
    email = request.cookies.get('cobertura_email')
    twitter_tag = conf.SEMINARIO_TWITTER_TAG
    cid = conf.SEMINARIO_CATEGORIA_ID
    pagination, posts = fromcache("seminario_posts") or tocache("seminario_posts", wordpress.getPostsByCategory(cat=cid))
    
    twites = []
    try:
        twites = fromcache("seminario_twitts") or tocache("seminario_twitts", twitts(hashtag=twitter_tag, count=5) )
    except Exception as e:
        print "ERRO AO BUSCAR OS TWITTS"
        print e

    # photos = fromcache('seminario_flickr') or tocache('seminario_flickr',get_flickr_photos())
    instaphotos = fromcache('seminario_insta') or tocache('seminario_insta', get_instagram_photos())
    links = LinkColaborativo.query.order_by(LinkColaborativo.id.desc())

    y = re.compile("http[s]*:.*youtube.com/watch.*")
    f = re.compile("http[s]*:.*flickr.com/.*")

    # pdb.set_trace()
    totallist = []
    for link in links:
        link.objeto = "link"
        if y.match(link.link):
            link.tipo = 'youtube'
        elif f.match(link.link):
            link.tipo = 'flickr'
        else:
            link.tipo = 'normal'
        totallist.append(link)
    # pdb.set_trace()
    for photo in instaphotos:
        photo['objeto'] = "instagram"
        totallist.append(photo)
    # pdb.set_trace()
    for tw in twites:
        tw['objeto'] = "twitter"
        tw['datetime'] = tw['created_at']
        totallist.append(tw)
    # pdb.set_trace()
    for post in posts:
        post.objeto = "post"
        post.datetime = post.the_date
        totallist.append(post)

    # print posts
    totallist = sorted(totallist,key=lambda i: i['datetime'] if type(i) is dict else i.datetime)

    return render_template('cobertura.html', posts=posts, twitts=twites,
        instaphotos=instaphotos, nome=nome, email=email, links=links, totallist=totallist)


@seminario.route('/av',methods=['POST'])
def av():
    """Metodo que conta os clicks em cada link colaborativo"""
    id = request.form['i']
    link = LinkColaborativo.get(id)
    link.clicks = link.clicks + 1
    dbsession.add(link)
    dbsession.commit()
    return ""


@seminario.route('/inscrever', methods=['POST'])
def inscrever():

    resp = {'status':0, 'msg':'Obrigado pela sua inscrição'}
    try:

        if not request.form['nome'] or not request.form['email']:
            resp['status'] = 2
            resp['msg'] = 'É necessário preencher o Nome e o Email'
        else:
            insc = InscricaoSeminario()
            insc.nome = request.form['nome']
            insc.email = request.form['email']
            insc.telefone = request.form['telefone']
            insc.twitter = request.form['twitter']
            insc.facebook = request.form['facebook']
            insc.site = request.form['site']

            dbsession.add(insc)
            dbsession.commit()

            try:
                sendmail(conf.SEMINARIO_SUBJECT % {'nome':request.form['nome']}
                    , request.form['email'], conf.SEMINARIO_MSG)
            except Exception as e:
                print e
                print "Erro ao enviar email para", request.form['email']
                pass

    except IntegrityError as i:
        resp['msg'] = "Este email informado já está cadastrado em nossa base de dados."
        resp['status'] = 1
        dbsession.rollback()
    except Exception as e:
        print e
        resp['msg'] = "Ocorreu algum problema ao efetuar sua insrição. Tente novamente logo mais ou fale com os organizadores."
        resp['status'] = -1
        dbsession.rollback()

    return jsonify(resp)

@seminario.route('/getitle/', methods=['POST','GET'])
def getitle():
    import urllib2
    import re
    site = request.args['site'] or request.form['site']

    s = urllib2.urlopen(site)
    html = s.read()
    titleRE = re.compile("<title>(.+?)</title>")

    # print html
    # print titleRE.search(html)

    title = titleRE.search(html.replace('\n','')).group(1).strip()

    return jsonify({'title':title})

@seminario.route('/newlink/', methods=['POST'])
def newlink():
    try:
        link = LinkColaborativo()
        link.nome = request.form['nome']
        link.email= request.form['email']
        link.link= request.form['link']
        link.site= request.form['nomedosite']
        link.imagem= request.form['linkimagem']
        link.clicks = 0

        dbsession.add(link)
        dbsession.commit()

        r = jsonify({'status':0, 'msg':'Obrigado pela sua contribuição!'})
        r.set_cookie('cobertura_nome', request.form['nome'])
        r.set_cookie('cobertura_email', request.form['email'])
        return r

    except IntegrityError as i:
        print "TENTOU SALVAR UM LINK QUE JÁ EXISTE"
        return jsonify({'status':1, 'msg':'Este link já foi divulgado em nosso site'})
    except Exception as e:
        print "ERRO AO SALVAR NOVO LINK COLABORATIVO"
        print e
        return jsonify({'status':-1, 'msg':'Ocorreu um erro ao processar o seu envio. Tente novamente ou avise os administradores.'})
