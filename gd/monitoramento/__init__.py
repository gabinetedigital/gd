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
from flask import Blueprint, request, render_template, redirect, \
    url_for, abort, current_app

# from gd.utils import msg, format_csrf_error
from gd.content import wordpress
from gd.utils.gdcache import cache, fromcache, tocache, removecache
from gd import conf

monitoramento = Blueprint(
    'monitoramento', __name__,
    template_folder='templates',
    static_folder='static')

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')

def _get_obras():
	obras = wordpress.monitoramento.getObras()
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
	# print "OBRAS =========================================================================="
	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	return render_template('monitoramento.html',
		obras=obras,
		menu=menus,
		twitter_hash_cabecalho=twitter_hash_cabecalho,
	)

@monitoramento.route('/obra/<slug>/')
def obra(slug):
	menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
	try:
		twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
	except KeyError:
		twitter_hash_cabecalho = ""

	return render_template('obra.html',
		menu=menus,
		twitter_hash_cabecalho=twitter_hash_cabecalho
	)
