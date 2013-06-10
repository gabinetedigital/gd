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

import os
import re
import xmlrpclib
from hashlib import md5

# from gd.auth import is_authenticated, authenticated_user #, NobodyHome
from gd import auth as authapi
from gd.utils import dumps, sendmail, send_welcome_email
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

def _get_stats(obraid=None):
	"""
	Método que retorna os dados estatísticos sobre a quantidade de obras e votos...
	"""
	return {
             'total_filhos_'+str(obraid) : wordpress.monitoramento.getObraStatsFilhos(obraid) if obraid else 0,
             'total_filhos_geral':wordpress.monitoramento.getObraStatsFilhos(),
             'total_votos_geral': wordpress.monitoramento.getObraStatsVotos()
	       }


def _get_obras(slug=None, obraid=None):
	if slug:
		obras = [wordpress.monitoramento.getObra(slug)]
	elif obraid:
		obras = [wordpress.monitoramento.getObraById(obraid)]
	else:
		obras = wordpress.monitoramento.getObras()

	# print "="*40
	# print obras
	# print "="*40

	return adjustCf(obras)


def adjustCf(obras):
	"""#Trata o retorno dos custom_fields para facilitar a utilizacao"""
	r_obras = []
	for obra in obras:
		if obra['custom_fields']:
			custom_fields = {}
			for cf in obra['custom_fields']:
				valor = cf['value']
				#=== tratamento especial para alguns custom fields
				if cf['key'] == 'gdvideo':
					vid = valor
					video = fromcache("video_%s" % str(vid)) or tocache("video_%s" % str(vid), wordpress.wpgd.getVideo(vid))
					sources = fromcache("video_src_%s" % str(vid)) or tocache("video_src_%s" % str(vid),wordpress.wpgd.getVideoSources(vid))
					# print "SOURCES===", sources

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
					# print "SOURCES===", video_sources
					valor = video


				if cf['key'] in ( 'gdobra_empresa_contratada', 'gdobra_municipio' ):
					#Deixa somente os nomes das empresas contratadas
					valor = [ x[1:-1] for x in re.findall('"[\wáéíóúàèìòùüëãõ ]*"',valor) ]

				if cf['key'] == 'gdobra_coordenadas' :
					# print "LLLLLLLL", "[" + valor + "]"
					valor = re.findall("([\+-].\d+.\d+,[\+-].\d+.\d+)", valor)

				custom_fields[cf['key']] = valor
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

	"""
		Os slides que aparecem da capa do Monitoramento são Páginas filhas de uma página com slug 'capa-obras'.
		Com título e conteúdo de texto.
		- Se tem imagem destacada, mostra-a no thumbnail
		- Se tem custom_field "gdvideo" busca o video no sistema de videos do GD
		- Se tem custom_field "youtube" busca o thumbnail do youtube através do VideoID
		- Se tem custom_field "video" , contendo o endereco de um video qualquer, usa a imagem destacada como thumbnail também.
	"""

	retslides = []
	for slide in slides:
		#Trata o retorno dos custom_fields para facilitar a utilizacao
		if slide['custom_fields']:
			custom_fields = {}
			for cf in slide['custom_fields']:
				custom_fields[cf['key']] = cf['value']
			del slide['custom_fields']
			slide['custom_fields'] = custom_fields

			# print "SLIDE===", slide
			if slide['custom_fields'].has_key('gdvideo'):
				vid = slide['custom_fields']['gdvideo']
				video = fromcache("video_%s" % str(vid)) or tocache("video_%s" % str(vid), wordpress.wpgd.getVideo(vid))
				sources = fromcache("video_src_%s" % str(vid)) or tocache("video_src_%s" % str(vid),wordpress.wpgd.getVideoSources(vid))
				# print "SOURCES===", sources

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
				# print "SOURCES===", video_sources
				slide['gdvideo'] = video

			if slide['custom_fields'].has_key('youtube'):
				video = slide['custom_fields']['youtube']
				# Espera algo como: https://www.youtube.com/watch?v=IuW_gf7hQTE
				s = re.search(r'(v=)([A-Za-z0-9_]+)', video)
				if s:
					yid =  s.groups()[1]
				else:
					yid = False

				if yid:
					thumb = "http://img.youtube.com/vi/%s/0.jpg" % yid
					video = {'video': video, 'thumb': thumb}
					slide['youtube'] = video

			if slide['custom_fields'].has_key('video'):
				slide['video'] = slide['custom_fields']['video']

		retslides.append(slide)

	# print "OBRAS SLIDES ==========================================================================", len(slides)

	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	try:
		valor_investimentos = conf.VALOR_INVESTIMENTOS
	except KeyError:
		valor_investimentos = ""

	return render_template('monitoramento.html',
		obras=obras,
		slides=retslides,
		stats=_get_stats(),
		milhoes=valor_investimentos,
		menu=menus,
		twitter_hash_cabecalho=twitter_hash_cabecalho,
	)


@monitoramento.route('/obra/<slug>/item/<itemid>/')
def timelineitem(slug, itemid):
	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	cacheid = "obratl%s-%s"%(obra['id'],itemid)
	timeline = fromcache(cacheid) or tocache(cacheid, wordpress.monitoramento.getObraTimeline(obra['id'], int(itemid) ))
	timeline = adjustCf(timeline)
	update = timeline[0]

	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	howto = fromcache('howtoobras') or tocache('howtoobras',wordpress.getPageByPath('howto-obras'))
	tos = fromcache('tosobras') or tocache('tosobras',wordpress.getPageByPath('tos-obras'))
	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	return render_template('timeline-item.html',
		menu=menus,
		obra=obra,
		howto=howto,
		tos=tos,
		update=update,
		twitter_hash_cabecalho=twitter_hash_cabecalho
	)


@monitoramento.route('/obra/<obraid>/<slug>/<plus>/')
def vote(obraid, slug, plus):
	"""
	O controle do voto é como segue:
	 - obraid = É o id do item da timeline (post-filho) que está sendo votado
	 - slug   = É um md5 criado através do slug do post-filho
	 - plus   = É um md5 criado através do obraid juntamente com:
	            ->  1 se for para somar voto
	            -> -1 se for para dominuir voto
	"""

	ret = {}

	post = wordpress.getCustomPost(obraid, 'gdobra')

	# print "Post", post['id'], post['post_type']

	post_slug = md5(post['slug']).hexdigest()
	slugok = True if post_slug == slug else False
	# print "SLUG===", slug, type(post_slug), post['slug'], type(post['slug'])

	md5_plus = md5(obraid + '1').hexdigest()
	md5_down = md5(obraid + '-1').hexdigest()
	vote_plus = True if md5_plus == plus else False
	vote_down = True if md5_down == plus else False

	# print "PLUS===", plus, md5_plus
	# print "DOWN===", plus, md5_down

	# print "Votando", slugok, vote_plus, vote_down

	item      = "gdobra_"
	itemup    = item+"voto_up"
	itemdown  = item+"voto_down"
	itemscore = item+"voto_score"
	itemvoted = item+"users_voted"

	if 'custom_fields' in post:
		cfs = post['custom_fields']

		# print "Custom Fields", cfs

		score = [ int(f['value']) for f in cfs if f['key'] == itemscore]
		votosup = [ int(f['value']) for f in cfs if f['key'] == itemup]
		votosdown = [ int(f['value']) for f in cfs if f['key'] == itemdown]
		users_voted = [ int(f['value']) for f in cfs if f['key'] == itemvoted]

		score = score[0] if score else 0
		votosup = votosup[0] if votosup else 0
		votosdown = votosdown[0] if votosdown else 0
		users_voted = users_voted[0] if users_voted else ""

		if vote_plus:
			score += 1
			votosup += 1
		else:
			score -= 1
			votosdown += 1

		ret['score'] = score

		feito = ""
		newcfs = []
		for cf in cfs :
			if cf['key'] == itemscore:
				cf['value'] = score
				feito+=",%s" % itemscore
				newcfs.append(cf)
			if cf['key'] == itemup:
				cf['value'] = votosup
				feito+=",%s" % itemup
				newcfs.append(cf)
			if cf['key'] == itemdown:
				cf['value'] = votosdown
				feito+=",%s" % itemdown
				newcfs.append(cf)
		if itemscore not in feito:
			newcfs.append({'key':itemscore, 'value':score})
		if itemup not in feito:
			newcfs.append({'key':itemup, 'value':votosup})
		if itemdown not in feito:
			newcfs.append({'key':itemdown, 'value':votosdown})

		# print "Custom Fields OK", newcfs

		#Grava o usuário que votou
		users_voted = users_voted + authapi.authenticated_user().username + ","
		newcfs.append({'key':itemvoted, 'value':users_voted})

		# edit_post_id = wordpress.wp.editPost(
		# 	post_id=post['id'],
		# 	custom_fields = cfs
		# )
		edit_post_id = wordpress.exapi.setPostCustomFields(post['id'], newcfs)

	return dumps(ret)


@monitoramento.route('/obra/<slug>/')
def obra(slug):
	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	cacheid = "obratl-%s"%slug
	timeline = fromcache(cacheid) or tocache(cacheid,wordpress.monitoramento.getObraTimeline(obra['id']))
	timeline = adjustCf(timeline)

	cacheid = "page-more-"+slug
	more = fromcache(cacheid) or tocache(cacheid,wordpress.getPageByPath('more-'+slug))
	if more:
		more = more.content

	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	tos = fromcache('tosobras') or tocache('tosobras',wordpress.getPageByPath('tos-obras'))
	howto = fromcache('howtoobras') or tocache('howtoobras',wordpress.getPageByPath('howto-obras'))
	return render_template('obra.html',
		menu=menus,
		obra=obra,
		tos=tos,
		howto=howto,
		more=more,
		timeline=timeline,
		twitter_hash_cabecalho=twitter_hash_cabecalho
	)


@monitoramento.route('/obra/part/<obra_slug>/<int:statusid>')
def timelineplus(obra_slug, statusid):
	cacheid = "obratl-%s"%obra_slug
	obra = fromcache("obra-" + obra_slug) or tocache("obra-" + obra_slug, _get_obras(obra_slug)[0])
	timeline = fromcache(cacheid) or tocache(cacheid,wordpress.monitoramento.getObraTimeline(obra['id']))
	timeline = adjustCf(timeline)
	# import pdb

	updates = []
	# pdb.set_trace()
	inrange = False
	for resp in timeline:
		# print statusid, resp['id'], resp['format']
		if int(resp['id']) == statusid and resp['format'] == 'status':
			inrange = True
		elif resp['format'] == 'status' and inrange:
			inrange = False
			# break
		if inrange:
			# print "Added!"
			updates.append(resp)

	return render_template('timeline_part.html', timeline=updates, obra=obra)
	# return "Mais um item... %s " % statusid


@monitoramento.route('/obra/seguir/<obraid>', methods=('POST',))
def seguir(obraid):

	emailto = ""
	obra = fromcache("obra-" + obraid) or tocache("obra-" + obraid, _get_obras(obraid=obraid)[0])

	if not obra:
		print "Não achou a obra!"
		return abort(404)

	slug = obra['slug']

	if request.form:
		follow = UserFollow()

		if authapi.is_authenticated():
			follow.user = authapi.authenticated_user()
			emailto = follow.user.email

		follow.obra_id = int(obraid)

		if request.form.has_key('faceid'):
			follow.facebook_id = request.form['faceid']

		if request.form.has_key('twitterid'):
			follow.twitter_id = request.form['twitterid']

		if request.form.has_key('email'):
			follow.email = request.form['email']
			emailto = follow.email

		dbsession.commit()

		if emailto:
			base_url = current_app.config['BASE_URL']
			base_url = base_url if base_url[-1:] != '/' else base_url[:-1] #corta a barra final
			data = {
				'titulo': obra['title'],
				'link'  : base_url + url_for('.obra',slug=slug),
				'descricao' : Markup(obra['content']).striptags(),
				'monitore_url': base_url + url_for('.index'),
				'siteurl': base_url,
			}
	        sendmail(
	            current_app.config['SEGUIROBRA_SUBJECT'] % data,
	            emailto,
	            current_app.config['SEGUIROBRA_MSG'] % data
	        )


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

	r = {'status':'ok', 'message':'Sua contibuição foi aceita com sucesso'}
	user_recent = False
	if not authapi.is_authenticated():
		# r = {'status':'not_logged'}
		"""
		Se não está autenticado, tenta achar o usuário pelo email, e
		acessar com a senha inserida no formulario.
		Se não, cadastra o camarada, com o nome e email informados, gerando
		uma senha para ele e enviando o email de boas vindas.
		"""
		email = request.form['email']

		if request.form['senha']:
			#Informou a senha do cadastro já existente
			# username = email
			# senha = request.form['senha']
			#Efetua o login
			print "Usuario e senha informado... logando!"
			username = request.values.get('email')
			senha = request.values.get('senha')
			print "tentando logar com", username, senha
			try:
				user = authapi.login(username, senha)
				r = {'status':'ok', 'message':'Sua contibuição foi aceita com sucesso', 'refresh': True}
			except authapi.UserNotFound:
				r = {'status':'nok', 'message':_(u'Wrong user or password')}
				return dumps(r)
			except authapi.UserAndPasswordMissmatch:
				r = {'status':'nok', 'message':_(u'Wrong user or password')}
				return dumps(r)
		elif request.form['nome']:
			print "Nome informado... cadastrando..."
			#Informou a senha para cadastro
			nome = request.form['nome']
			telefone = request.form['telefone'] if 'telefone' in request.form else ""
			novasenha = request.form['newPassword'] if 'newPassword' in request.form else ""

			if not novasenha:
				novasenha = "gabinetedigital"

			# print nome, '-', email, '-', novasenha

			try:
				user = authapi.create_user(nome, email, unicode(novasenha), email)
				r = {'status':'ok', 'message':'Sua contibuição foi aceita com sucesso. Verifique seu email para confirmar o cadastro.'}
				user_recent = True
				send_welcome_email(user)
			except authapi.UserExistsUnconfirmed, e:
				r = {'status':'nok', 'message':u'Seu usuário precisa ser confirmado, veja seu email!'}
				return dumps(r)

			if telefone:
				user.set_meta('phone', telefone)
				dbsession.commit()
	else:
		print "JAH ESTAVA LOGADO!"
		user = authapi.authenticated_user()


	if authapi.is_authenticated() or user_recent:

		print ">>>>>>>>>>>> SALVANDO CONTRIBUIÇÃO ..."
		print user

		author_id = user.id
		status    = "pending"

		ultimo_status = wordpress.monitoramento.getUltimaRespostaGovObra(obra['id'])
		print "Achou o ultimo status publico da obra:"
		print ultimo_status

		if request.form['link'] :
			#Contribuição em texto
			print "COM VIDEO -------------"
			new_post_id = wordpress.wp.newPost(
				post_title    = request.form['titulo'],
				post_type     = "gdobra",
				post_parent   = ultimo_status['id'],
				post_author   = author_id, #int
				post_content  = request.form['conteudo'],
				post_status   = status,
				post_format   = "video",
				custom_fields = [
									{ 'key': 'gdobra_video', 'value': request.form['link'] }
								]
			)
		else:

			if request.files:
				#Contribuição imagem

				foto = request.files['foto']
				if foto and allowed_file(foto.filename):
					filename = secure_filename(foto.filename)
					file_path = os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], filename)
					foto.save(file_path)
					file = open(file_path)
					base64bits = xmlrpclib.Binary(file.read())
					media = wordpress.wp.uploadFile(name=file_path, type=foto.content_type, bits=base64bits, overwrite=False)

					new_post_id = wordpress.wp.newPost(
						post_title    = request.form['titulo'],
						post_type     = "gdobra",
						post_parent   = ultimo_status['id'],
						post_author   = author_id, #int
						post_content  = request.form['conteudo'],
						post_status   = status,
						post_format   = "image",
						post_thumbnail= int(media['id']), #int
					)

				else:
					r = {'status':'ok', 'message':'O arquivo enviado não é permitido. Use apenas arquivos PNG ou JPG.'}

			else:
				#Contribuição somente texto
				print "TEXTO <-------------"
				new_post_id = wordpress.wp.newPost(
					post_title    = request.form['titulo'],
					post_type     = "gdobra",
					post_parent   = ultimo_status['id'],
					post_author   = author_id, #int
					post_content  = request.form['conteudo'],
					post_status   = status,
					post_format   = "video" if request.files else "aside"
				)


	return dumps(r)


#=================================================================== API ======
@monitoramento.route('/api/obras.json',methods=('GET',))
def api_obras():
	obras = fromcache("obras-monitoramento") or tocache("obras-monitoramento", _get_obras())
	return Response(dumps(obras),content_type="application/json")

@monitoramento.route('/api/obras/<obraid>.json',methods=('GET',))
def api_obraid(obraid):
	# obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	obra = wordpress.getCustomPost(obraid, 'gdobra')
	if not obra:
		return Response(dumps({'status':'invalid_obraid'}),content_type="application/json")

	# timeline = wordpress.monitoramento.getObraTimeline(obra['id'], int(itemid) )
	# timeline = adjustCf(timeline)
	# update = timeline[0]

	return Response(dumps(obra),content_type="application/json")

#=================================================================== API ======
