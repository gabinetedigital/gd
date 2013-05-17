# -*- coding:utf-8 -*-
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
from flask import Blueprint, request, render_template, abort, current_app
from werkzeug import secure_filename

import os
import xmlrpclib

from gd.auth import is_authenticated, authenticated_user #, NobodyHome
from gd.utils import dumps
from gd.model import UserFollow, session as dbsession
from gd.content import wordpress
from gd.utils.gdcache import fromcache, tocache #, cache, removecache
from gd import conf

monitoramento = Blueprint(
    'monitoramento', __name__,
    template_folder='templates',
    static_folder='static')

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def _get_obras(slug=None):
	if not slug:
		obras = wordpress.monitoramento.getObras()
	else:
		obras = [wordpress.monitoramento.getObra(slug)]

	print "="*40
	print obras
	print "="*40

	r_obras = []
	for obra in obras:
		#Trata o retorno dos custom_fields para facilitar a utilizacao
		if obra['custom_fields']:
			custom_fields = {}
			for cf in obra['custom_fields']:
				custom_fields[cf['key']] = cf['value']
			del obra['custom_fields']
			obra['custom_fields'] = custom_fields
		r_obras.append(obra)

	return r_obras


@monitoramento.route('/')
def index():

	obras = fromcache("obras-monitoramento") or tocache("obras-monitoramento", _get_obras())
	# print "OBRAS =========================================================================="
	# print obras
	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	slides = wordpress.getPagesByParent('capa-obras',thumbsizes=['slideshow','thumbnail']);

	for slide in slides:
		#Trata o retorno dos custom_fields para facilitar a utilizacao
		if slide['custom_fields']:
			custom_fields = {}
			for cf in slide['custom_fields']:
				custom_fields[cf['key']] = cf['value']
			del slide['custom_fields']
			slide['custom_fields'] = custom_fields

			# pdb.set_trace()
			print slide
			if slide['custom_fields'].has_key('gdvideo'):
				vid = slide['custom_fields']['gdvideo']
				video = fromcache("video_%s" % str(vid)) or tocache("video_%s" % str(vid), wordpress.wpgd.getVideo(vid))
				sources = fromcache("video_src_%s" % str(vid)) or tocache("video_src_%s" % str(vid),wordpress.wpgd.getVideoSources(vid))

				base_url = current_app.config['BASE_URL']
				base_url = base_url if base_url[-1:] != '/' else base_url[:-1] #corta a barra final
				video_sources = {}
				for s in sources:
				    if(s['format'].find(';') > 0):
				        f = s['format'][0:s['format'].find(';')]
				    else:
				        f = s['format']
				    video_sources[f] = s['url']
				video['sources'] = video_sources
				slide['video'] = video

	print "OBRAS SLIDES ==========================================================================", len(slides)

	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	return render_template('monitoramento.html',
		obras=obras,
		slides=slides,
		menu=menus,
		twitter_hash_cabecalho=twitter_hash_cabecalho,
	)

@monitoramento.route('/obra/<slug>/')
def obra(slug):
	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	timeline = wordpress.monitoramento.getObraTimeline(obra['id'])
	print "="*50
	print timeline
	print "="*50

	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	return render_template('obra.html',
		menu=menus,
		obra=obra,
		timeline=timeline,
		twitter_hash_cabecalho=twitter_hash_cabecalho
	)


@monitoramento.route('/obra/<obraid>/seguir',methods=('POST',))
def seguir(obraid):

	if request.form:
		follow = UserFollow()

		if is_authenticated():
			follow.user = authenticated_user()

		follow.obra_id = int(obraid)

		if request.form.has_key('faceid'):
			follow.facebook_id = request.form['faceid']

		if request.form.has_key('twitterid'):
			follow.twitter_id = request.form['twitterid']

		if request.form.has_key('email'):
			follow.email = request.form['email']

		dbsession.commit()

		return dumps({'status':'ok'})
	else:
		return dumps({'status':'error'})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@monitoramento.route('/obra/<slug>/contribui', methods=('POST',))
def contribui(slug):

	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	print request.form
	r = {'status':'ok'}

	if not is_authenticated():
		r = {'status':'not_logged'}

	else:

		author_id = authenticated_user().id
		status    = "pending"

		if request.form['tipo'] == 't':
			#Contribuição em texto
			print "TEXTO <-------------"
			new_post_id = wordpress.wp.newPost(
				post_title    = request.form['titulo'],
				post_type     = "gdobra",
				post_parent   = obra['id'],
				post_author   = author_id, #int
				post_content  = request.form['conteudo'],
				post_status   = status,
				post_format   = "aside",
			)

		if request.form['tipo'] == 'v':
			#Contribuição em video
			print "VIDEO <-------------"
			new_post_id = wordpress.wp.newPost(
				post_title    = request.form['titulo'],
				post_type     = "gdobra",
				post_parent   = obra['id'],
				post_author   = author_id, #int
				post_content  = request.form['link'],
				post_status   = status,
				post_format   = "video",
				# post_thumbnail=0, #int
			)

		if request.form['tipo'] == 'f':
			#Contribuição em foto
			#print "FOTO <-------------"

			if request.files:
				#print "Arquivos", request.files['foto']
				foto = request.files['foto']
				if foto and allowed_file(foto.filename):
					#print "Foto permitida"
					filename = secure_filename(foto.filename)
					file_path = os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], filename)
					#print "Salvando", file_path
					foto.save(file_path)
					file = open(file_path)
					base64bits = xmlrpclib.Binary(file.read())
					#print "Enviando foto..."
					media = wordpress.wp.uploadFile(name=file_path, type=foto.content_type, bits=base64bits, overwrite=False)

					#print "Media uploaded", media['id'], media

					new_post_id = wordpress.wp.newPost(
						post_title    = request.form['titulo'],
						post_type     = "gdobra",
						post_parent   = obra['id'],
						post_author   = author_id, #int
						# post_content  = request.form['conteudo'],
						post_status   = status,
						post_format   = "image",
						post_thumbnail= int(media['id']), #int
					)

					#print "--> Novo post", new_post_id, "gravado!"
				else:
					#print "Nao PERMITIDO!"
					r = {'status':'file_not_allowed'}
			else:
				#print "Nao ENCONTRADO!"
				r = {'status':'file_not_found'}

	return dumps(r)

