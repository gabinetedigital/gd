# -*- coding:utf-8 -*-
#
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
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

from flask import Blueprint, render_template
from gd.content.wp import wordpress, gallery

balanco = Blueprint(
    'balanco', __name__,
    template_folder='templates',
    static_folder='static')


@balanco.route('/')
def index():
    # First page data
    pagination, posts = wordpress.getPostsByTag(
        tag='governador-pergunta')
    images = gallery.search('GovernadorPergunta', limit=24)[::-1]
    videos = [wordpress.wpgd.getVideo(i) for i in (14, 16, 12)]
    return render_template(
        'balanco.html', posts=posts, images=images, videos=videos,
        pagename='govpergunta'
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal')
    )


@balanco.route('/govresponde/')
def govresponde():
    return render_template(
        'balanco_govresponde.html',
        pagename='govresponde',
        videos=[wordpress.wpgd.getVideo(i) for i in range(17, 23)]
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal')
    )


@balanco.route('/govescuta/')
def govescuta():
    imgs = {
        'bullying': gallery.search('bullying'),
        'estrangeirismo': gallery.search('estrangeirismo'),
        'softwarelivre': gallery.search('software-livre'),
    }
    return render_template(
        'balanco_govescuta.html',
        pagename='govescuta',
        imgs=imgs
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal')
    )


@balanco.route('/agenda/')
def agenda():
    images = {
        'bage': gallery.search('bagé'),
        'santana': gallery.search('santana-do-livramento'),
        'esteio': gallery.search('esteio'),
        'taquara': gallery.search('taquara'),
    }
    return render_template(
        'balanco_agenda.html',
        pagename='agenda',
        images=images
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal')
    )
