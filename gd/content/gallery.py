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

from flask import Blueprint, render_template, abort, request, jsonify, send_from_directory, current_app, redirect, url_for
from gd.content.wp import wordpress, gallery as api
import math
import urllib2

gallery = Blueprint(
    'gallery', __name__,
    template_folder='templates',
    static_folder='static')

@gallery.route('/<slug>/')
def galerias(slug=None):
    galleries = wordpress.wpgd.getGalleries()
    if slug and (str(slug) not in [i['slug'] for i in galleries]):
        abort(404)
    current = wordpress.wpgd.getGallery(slug or galleries[0]['slug'])
    titulos = [ (g['slug'],g['title']) for g in galleries ]
    try:
        twitter_hash_cabecalho = current_app.config['TWITTER_HASH_CABECALHO']
    except KeyError:
        twitter_hash_cabecalho = ""

    return render_template(
        'gallery.html',
        current=current,
        twitter_hash_cabecalho=twitter_hash_cabecalho,
        menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal'),
        titulos=titulos,
    )


@gallery.route('/')
def index(slug=None):
    search_terms = ''
    if 's' in request.args and request.args.get('s', ''):
        search_terms = request.args.get('s', '')
        galleries = wordpress.wpgd.searchGalleries('%s' % search_terms)
        if len(galleries) == 1:
            return redirect(url_for('.galerias', slug=galleries[0]['slug']))
    else:
        galleries = wordpress.wpgd.getGalleries()
        if not galleries:
            abort(404)
    current = None

    titulos = [ (g['slug'],g['title']) for g in galleries ]
    try:
        twitter_hash_cabecalho = current_app.config['TWITTER_HASH_CABECALHO']
    except KeyError:
        twitter_hash_cabecalho = ""

    return render_template(
        'gallerys.html',
        galleries=galleries,
        s=search_terms,
        twitter_hash_cabecalho=twitter_hash_cabecalho,
        menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal'),
        titulos=titulos) 

@gallery.route('/vote/<int:gid>/')
@gallery.route('/vote/<int:gid>/<int:rate>/')
def vote(gid, rate=-1):
    try:
        can = wordpress.nggv.canVoteGallery( gid )
        if can in ['true','True',True]:
            if rate == -1:
                rate = request.args.get('value', -1, type=int)
                if rate != -1:
                    vote_result = wordpress.nggv.voteGallery( gid, rate )
        else:
            vote_result = 'False'
        return jsonify( "{'vote': '%s', 'msg': %s }" % ( str(vote_result), can ) )
    except RuntimeError as e:
        print e.errno, e.strerror
        return jsonify("{'vote': 'False', 'msg': ''}")

@gallery.route('/fotoDownload/<gallery>/<string:filename>')
def fotoDownload(gallery=None,filename=None):
    arquive_url = "%s/wp-content/gallery/%s/%s" % (current_app.config['WORDPRESS_ADDRESS'], gallery, filename)
    print arquive_url
    # arq = arquive_url
    # nomearq = arq.replace("$", "/")
    # arq = str(nomearq)
    # nomearq = str.split(arq, '/')
    # nomearq = nomearq[len(nomearq)-1]
    # nomearq = nomearq.replace("_backup", "")
    u = urllib2.urlopen(arquive_url)
    localFile = open('/tmp/'+filename, 'wb')
    localFile.write(u.read())
    localFile.close()

    return send_from_directory("/tmp",filename, as_attachment=True)
    
