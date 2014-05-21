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
from flask import Blueprint, request, render_template, abort, current_app, Response, url_for, redirect
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from jinja2.utils import Markup
# from twython import Twython

import datetime as d
import os
import re
import xmlrpclib
import traceback
import random
import string
import pdb
from hashlib import md5

# from gd.auth import is_authenticated, authenticated_user #, NobodyHome
from gd import auth as authapi
from gd.utils import dumps, sendmail, send_welcome_email, send_password, twitts, get_twitter_connection, treat_categories
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


def _get_obras(slug=None, obraid=None, slim=False, filtros=None):
	if slug:
		obras = [wordpress.monitoramento.getObra(slug)]
	elif obraid:
		obras = [wordpress.monitoramento.getObraById(obraid)]
	else:
		# print ">>>>>>>>>>>>>>>>>> GET TODAS AS OBRAS"
		obras = wordpress.monitoramento.getObras(filtros)

	# print "="*40
	# print obras
	# print "="*40
	if not slim:
		return adjustCf(obras)
	else:
		return obras


def adjustCf(obras):
	"""#Trata o retorno dos custom_fields para facilitar a utilizacao"""
	r_obras = []
	for obra in obras:
		# print "--->>>", obra['title'], obra['date']['date']
		if obra['custom_fields']:
			custom_fields = {}
			for cf in obra['custom_fields']:
				valor = cf['value']
				#=== tratamento especial para alguns custom fields
				if cf['key'] == 'gdvideo':
					vid = valor
					video = fromcache("video_%s" % str(vid)) or tocache("video_%s" % str(vid), treat_categories(wordpress.wpgd.getVideo(vid))[0])
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


				if cf['key'] in ( 'gdobra_municipio' ):
					#Deixa somente os nomes das empresas contratadas
					valor = [ x[1:-1] for x in re.findall('\".+?\"',valor) ]

				if cf['key'] in ( 'gdobra_empresa_contratada' ):
					#Deixa somente os nomes das empresas contratadas
					if '{' in valor:
						valor = [ x[1:-1] for x in re.findall('\".+?\"',valor) ]
					else:
						valor = [valor]

				if cf['key'] == 'gdobra_coordenadas' :
					# print "LLLLLLLL", "[" + valor + "]"
					valor = re.findall("([\+-].\d+.\d+,[\+-].\d+.\d+)", valor)

				custom_fields[cf['key']] = valor
			del obra['custom_fields']
			obra['custom_fields'] = custom_fields

		r_obras.append(obra)

	return r_obras

@monitoramento.route('/comments/<obraid>/')
def get_comments(obraid):
	cacheid = "cmts-item-obra-%s" % obraid
	cmts = fromcache(cacheid) or tocache(cacheid, wordpress.getComments(status='approve',post_id=obraid, number=1000) or [] )
	# if cmts:
	# 	cmts = cmts[::-1]
	# else:
	# 	cmts = []
	return render_template("comentarios.html", comentarios=cmts)


def get_cidades_das_obras():

	lcidades = []
	cidades = wordpress.monitoramento.getCidadesDasObras()

	for c in cidades:
		valor = [ x[1:-1] for x in re.findall('\".+?\"', c['meta_value'] ) ]
		for x in valor:
			if x.strip() not in lcidades:
				lcidades.append(x.strip())

	return sorted(lcidades)


@monitoramento.route('/', methods=("GET","POST"))
def index():

	filtros = {}
	if "filtro" in request.args or "ordem" in request.args:
		filtros = {
			'filtro': request.args['filtro'] if 'filtro' in request.args else "",
			'valor' : request.args['valor'] if 'valor' in request.args else "",
			'ordem' : request.args['ordem'] if 'ordem' in request.args else "atualizacao"
		}
	else:
		filtros = {
			'filtro': '',
			'valor' : '',
			'ordem' : 'atualizacao'
		}

	print ">>>>>>>>>>>>>>>>>>>>>>FILTROS::", filtros

	obras = fromcache("obras-monitoramento") or tocache("obras-monitoramento", _get_obras(filtros=filtros))
	# print "OBRAS =========================================================================="
	# print obras

	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	slides = wordpress.getPagesByParent('capa-obras',thumbsizes=['slideshow','thumbnail','full']);

	cidades = fromcache('cidades-das-obras') or tocache('cidades-das-obras', get_cidades_das_obras() )
	secretarias = fromcache('secretarias-das-obras') or tocache('secretarias-das-obras', wordpress.monitoramento.getSecretarias() )

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
				video = fromcache("video_%s" % str(vid)) or tocache("video_%s" % str(vid), treat_categories(wordpress.wpgd.getVideo(vid))[0])
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

	# try:
	# 	twitter_hash_cabecalho = twitts()
	# except KeyError:
	# 	twitter_hash_cabecalho = ""

	try:
		valor_investimentos = conf.VALOR_INVESTIMENTOS
	except KeyError:
		valor_investimentos = ""

	return render_template('deolho.html',
		obras=obras,
		cidades=cidades,
		secretarias=secretarias,
		slides=retslides,
		stats=_get_stats(),
		milhoes=valor_investimentos,
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

		# print "Custom Fields", [ f['value'] for f in cfs if f['key'] == itemvoted]

		score = [ int(f['value']) for f in cfs if f['key'] == itemscore]
		votosup = [ int(f['value']) for f in cfs if f['key'] == itemup]
		votosdown = [ int(f['value']) for f in cfs if f['key'] == itemdown]
		users_voted = [ f['value'] for f in cfs if f['key'] == itemvoted]

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
	print " >>>> BUSCANDO A OBRA por SLUG", slug
	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	cacheid = "obratl-%s"%slug
	print ">>>>>> BUSCANDO A TIMELINE DA OBRA PELO ID"
	timeline = fromcache(cacheid) or tocache(cacheid,wordpress.monitoramento.getObraTimeline(obra['id']))
	timeline = adjustCf(timeline)
	statuses = [ s for s in timeline if s['format'] == 'status' ]

	cacheid = "page-more-"+slug
	more = fromcache(cacheid) or tocache(cacheid,wordpress.getPageByPath('more-'+slug))
	if more:
		more = more.content

	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	try:
		twitter_hash_cabecalho = twitts()
	except KeyError:
		twitter_hash_cabecalho = ""

	tos = fromcache('tosobras') or tocache('tosobras',wordpress.getPageByPath('tos-obras'))
	howto = fromcache('howtoobras') or tocache('howtoobras',wordpress.getPageByPath('howto-obras'))
	obras = fromcache("obras-monitoramento-slim") or tocache("obras-monitoramento-slim", _get_obras(slim=True))
	return render_template('detalhe_obra.html',
		menu=menus,
		obra=obra,
		obras=obras,
		tos=tos,
		howto=howto,
		more=more,
		timeline=timeline,
		statuses=statuses,
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


@monitoramento.route('/obra/deseguir/<obraid>', methods=('POST',))
def deseguir(obraid):
	obra = fromcache("obra-" + obraid) or tocache("obra-" + obraid, _get_obras(obraid=obraid)[0])

	if not obra:
		print "Não achou a obra!"
		return abort(404)

	slug = obra['slug']

	if request.form:

		if request.form.has_key('faceid'):
			has = UserFollow.query.filter_by(obra_id=obraid, facebook_id=request.form['faceid'])
			if has.count() > 0:
				for f in has:
					has.delete()

		if request.form.has_key('twitterid'):
			has = UserFollow.query.filter_by(obra_id=obraid, twitter_id=request.form['twitterid'])
			if has.count() > 0:
				for f in has:
					has.delete()

		if request.form.has_key('email'):
			has = UserFollow.query.filter_by(obra_id=obraid, email=request.form['email'])
			if has.count() > 0:
				for f in has:
					has.delete()

		dbsession.commit()

		return dumps({'status':'ok', 'msg':u'Suas opções foram removidas. Obrigado por participar!'})
	else:
		return dumps({'status':'error'})

def _make_follow(obraid):
	follow = UserFollow()
	if authapi.is_authenticated():
		follow.user = authapi.authenticated_user()

	follow.obra_id = int(obraid)
	return follow


def _send_twitter_dm(twitterid, msg):
	tre = re.compile("(?P<link>(?:http(|s):\/\/)?(?:www.)?(twitter).com\/?)*(?P<nome>[\w\.\-]*)")
	if tre.match(twitterid):
		tid = tre.search(twitterid).group('nome')
	else:
		tid = u.twitter_id

	print "DE-OLHO-NAS-OBRAS::", tid
	try:
		t = get_twitter_connection()
		#send direct message
		t.create_friendship(screen_name=tid)
		dm = t.send_direct_message(
			user=tid,
			text=msg )
	except Exception as e:
		print "Ocorreu um erro enviando DM para twitter..."
		print e


@monitoramento.route('/obra/seguir/<obraid>', methods=('POST',))
def seguir(obraid):

	emailto = ""
	obra = fromcache("obra-" + obraid) or tocache("obra-" + obraid, _get_obras(obraid=obraid)[0])

	if not obra:
		print "Não achou a obra!"
		return abort(404)

	slug = obra['slug']

	if request.form:

		if request.form.has_key('faceid'):
			has = UserFollow.query.filter_by(obra_id=obraid, facebook_id=request.form['faceid'])
			if has.count() <= 0:
				# return dumps({'status':'error','msg':'Você já é seguidor desta obra pelo Facebook'})
				follow = _make_follow(obraid)
				follow.facebook_id = request.form['faceid']
				emailto = "%s@facebook.com" % follow.facebook_id

		if request.form.has_key('twitterid'):
			has = UserFollow.query.filter_by(obra_id=obraid, twitter_id=request.form['twitterid'])
			if has.count() <= 0:
				# return dumps({'status':'error','msg':'Você já é seguidor desta obra pelo Twitter'})
				follow = _make_follow(obraid)
				follow.twitter_id = request.form['twitterid']
				msg = u"A partir de agora você segue a obra %s!" % obra['title']
				_send_twitter_dm(follow.twitter_id, msg)

		if request.form.has_key('email'):
			has = UserFollow.query.filter_by(obra_id=obraid, email=request.form['email'])
			if has.count() <= 0:
				# return dumps({'status':'error','msg':'Você já é seguidor desta obra pelo Email'})
				follow = _make_follow(obraid)
				follow.email = request.form['email']
				emailto = follow.email

		dbsession.commit()

		if emailto:
			base_url = current_app.config['BASE_URL']
			base_url = base_url if base_url[-1:] != '/' else base_url[:-1] #corta a barra final
			_dados_email = {
				'titulo': obra['title'],
				'link'  : base_url + url_for('.obra',slug=slug),
				'descricao' : Markup(obra['content']).striptags(),
				'monitore_url': base_url + url_for('.index'),
				'siteurl': base_url,
			}
			sendmail(
			    current_app.config['SEGUIROBRA_SUBJECT'] % _dados_email,
			    emailto,
			    current_app.config['SEGUIROBRA_MSG'] % _dados_email
			)


		return dumps({'status':'ok'})
	else:
		return dumps({'status':'error'})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@monitoramento.route('/obra/<slug>/contribui', methods=('GET',))
def contribuir(slug):
	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	obras = fromcache("obras-monitoramento-slim") or tocache("obras-monitoramento-slim", _get_obras(slim=True))
	if not obra:
		return abort(404)
	return render_template("enviarContribuicao.html", obra=obra, obras=obras)


@monitoramento.route('/obra/<slug>/contribui', methods=('POST',))
def contribui(slug):

	obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
	if not obra:
		return abort(404)

	r = {'status':'ok', 'message':'Sua contibuição foi aceita com sucesso'}
	user_recent = False
	if not authapi.is_authenticated():
		r = {'status':'nok', 'message':u'É necessário estar logado para contribuir.'}
	else:
		print "JAH ESTAVA LOGADO!"
		user = authapi.authenticated_user()


	if authapi.is_authenticated() or user_recent:

		print ">>>>>>>>>>>> SALVANDO CONTRIBUIÇÃO ..."
		print user

		author_id = user.id if hasattr(user,'id') else user['id']
		# status    = "pending"
		status    = "publish"

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
				print "COM ARQUIVO %s -------------" % foto.filename

				if foto and allowed_file(foto.filename):

					filename = secure_filename(foto.filename)
					print "FOTO OK -------------"

					file_path = os.path.join(current_app.config['UPLOADS_DEFAULT_DEST'], filename)
					foto.save(file_path)
					file = open(file_path)
					base64bits = xmlrpclib.Binary(file.read())
					try:
						media = wordpress.wp.uploadFile(name=file_path, type=foto.content_type, bits=base64bits, overwrite=False)


						print "FOTO UPLOAD OK -------------"

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

						print "CONTRIB SALVA OK -------------"


					except xmlrpclib.ProtocolError, e:
						print "ERRO", e.errmsg
						if 'Too Large' in e.errmsg:
							r = {'status':'nok', 'message':'Esta imagem é muito grande para ser enviada.'}
						else:
							traceback.print_exc()
							r = {'status':'nok', 'message':'Ocorreu um erro ao processar a imagem.'}
					except :
						traceback.print_exc()
						r = {'status':'nok', 'message':'Ocorreu um erro ao processar sua contribuição.'}

				else:
					print "FOTO NAO PERMITIDA -------------"
					r = {'status':'nok', 'message':'O arquivo enviado não é permitido. Use apenas arquivos PNG ou JPG.'}

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

#=================================================================== ENVIO DE AVISOS DE ATUALIZAÇÕES

@monitoramento.route('/sendnews')
def sendnews():
	"""Método que faz o envio dos avisos para as pessoas que seguem as obras"""

	if "obra" in request.args:
		obraid = request.args['obra']
		obra = fromcache("obra-" + obraid) or tocache("obra-" + obraid, _get_obras(obraid=obraid)[0])
	elif "slug" in request.args:
		slug = request.args['slug']
		obra = fromcache("obra-" + slug) or tocache("obra-" + slug, _get_obras(slug)[0])
		obraid = obra['id']
	else:
		print "DE-OLHO-NAS-OBRAS::", "Não foi passado o ID nem o SLUG da obra para os avisos!"
		return abort(404)

	base_url = current_app.config['BASE_URL']
	obra_link = base_url + url_for('.obra',slug=obra['slug'])
	obra_titulo = obra['title']

	_dados_obra = {
		'titulo': obra_titulo,
		'link': obra_link
	}

	print "DE-OLHO-NAS-OBRAS::", "buscando usuarios"
	usuarios = UserFollow.query.filter(UserFollow.obra_id==int(obraid))

	ct = usuarios.count()
	if ct <= 0:
		print "DE-OLHO-NAS-OBRAS::", "Não existe nenhum usuario seguindo esta obra."
		return "Não existe nenhum usuário seguindo esta obra"

	print "DE-OLHO-NAS-OBRAS::", "Enviando aviso de atualizacoes para", ct,"usuarios."

	print "DE-OLHO-NAS-OBRAS::", "twitter connect"
	# t = Twython(current_app.config['TWITTER_CONSUMER_KEY'], current_app.config['TWITTER_CONSUMER_SECRET'],
	# 	current_app.config['TWITTER_ACCESS_TOKEN'], current_app.config['TWITTER_ACCESS_TOKEN_SECRET'])

	msg_titulo = current_app.config['OBRA_ATUALIZACAO_SUBJECT']
	msg = current_app.config['OBRA_ATUALIZACAO_MSG'] % _dados_obra
	msg_twitter = current_app.config['OBRA_ATUALIZACAO_TWITTER']

	for u in usuarios:
		# print "DE-OLHO-NAS-OBRAS::", u.obra_id, u.mode, u.facebook_id, u.twitter_id, u.email
		# print "USER:", u.user.email

		if u.facebook_id:
			print "DE-OLHO-NAS-OBRAS::", "Via facebook..."
			fre = re.compile("(?P<link>(?:http(|s):\/\/)?(?:www.)?(facebook|fb).com\/?)*(?P<nome>[\w\.\-]*)")

			if fre.match(u.facebook_id):
				fid = fre.search(u.facebook_id).group('nome')
			else:
				fid = u.facebook_id

			# print "DE-OLHO-NAS-OBRAS::", fid
			femail = "%s@facebook.com" % fid
			sendmail(msg_titulo, femail, msg)

		elif u.twitter_id:
			print "DE-OLHO-NAS-OBRAS::", "Via twitter..."
			msg = u"Tem atualização na obra %s! Veja: %s" % (obra_titulo, obra_link)
			_send_twitter_dm(u.twitter_id, msg)

		elif u.email:
			#sendmail
			print "DE-OLHO-NAS-OBRAS::", "Por email", u.email
			sendmail(msg_titulo, u.email, msg)

	print "DE-OLHO-NAS-OBRAS::", "Concluido!"
	return "Ok-" + d.datetime.now().strftime("%d%m%Y-%H%M%S") + "\n"


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
