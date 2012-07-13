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

from flask import Blueprint, render_template, abort, request
from gd.content.wp import wordpress, gallery as api

gallery = Blueprint(
    'gallery', __name__,
    template_folder='templates',
    static_folder='static')


@gallery.route('/')
@gallery.route('/<slug>')
def index(slug=None):
    search_terms = ''
    if 's' in request.args and request.args.get('s', ''):
        search_terms = request.args.get('s', '')
        galleries = wordpress.wpgd.searchGalleries('%s' % search_terms)
    else:
        galleries = wordpress.wpgd.getGalleries()
        if not galleries:
            abort(404)
    current = None
    if galleries:
        if slug and (str(slug) not in [i['slug'] for i in galleries]):
            abort(404)
        current = wordpress.wpgd.getGallery(slug or galleries[0]['slug'])
        
    return render_template(
        'gallery.html',
        galleries=galleries,
        s=search_terms,
        current=current)

@gallery.route('/vote/<int:imageid>/<int:rate>')
def vote(imageid, rate):
    try:
        can = wordpress.nggv.canVoteImage( imageid )
        if can == 'true':
            vote_result = wordpress.nggv.voteImage( imageid, rate )
        else:
            vote_result = 'False'
        return "{'vote': '%s' }" % str(vote_result)
    except RuntimeError as e:
        print e.errno, e.strerror
        return "{'vote': 'False'}"
