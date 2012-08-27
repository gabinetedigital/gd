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

from flask import Blueprint, request, render_template, redirect, \
    url_for, abort

from gd.content.wp import wordpress

govescuta = Blueprint(
    'govescuta', __name__,
    template_folder='templates',
    static_folder='static')


@govescuta.route('/')
@govescuta.route('/<int:page>')
def index(page=0):
#   audiences_raw, count = wordpress.gove.getAudiences(
#        'date',                    # sortby
#        '',                        # search
#        'audience.visible = true', # filter
#        '0',                       # page
#    )

#    audiences = []
#    for audience in audiences_raw[::-1]:
#        audience['video'] = wordpress.wpgd.getVideo(audience['data'])
#        audiences.append(audience)

#    return render_template(
#        'govescuta.html',
#        audiences=audiences,
#        count=count,
#    )
#
    sortby = request.values.get('sortby') or 'date'
    pagination, posts = wordpress.wpgove.getAudiencias(
                                            page=page, 
                                            sortby=sortby, 
                                            totalporpage='10')
#    pagination, posts = wordpress.wpgove.listAudiencia(wordpress.getPosts(page=page, 
#                                            post_type='audiencia_govesc' ))
#    pagination, posts = wordpress.getPosts(page=page, 
#                                           post_type='audiencia_govesc' )
    
#    audiencevideos = []
#    for post in posts:
#        audiencevideos.append(post.custom_fields)
    print 'leo == ', posts
    
    how_to = wordpress.getPageByPath('how-to-use-governo-escuta')    
        
    return render_template(
        'govescuta.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        audiences=posts,
        sortby=sortby,
#        audiencevideos=audiencevideos,
        how_to=getattr(how_to, 'content', ''),)

