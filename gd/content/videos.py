
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

from flask import Blueprint, render_template, current_app
from gd.content.wp import wordpress

videos = Blueprint(
    'videos', __name__,
    template_folder='templates',
    static_folder='static')


@videos.route('/')
def listing():
    videos = wordpress.wpgd.getVideos(
        where='status=true', orderby='date DESC')
    return render_template('videos.html', videos=videos
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal'))


@videos.route('/<int:vid>/')
def details(vid):
    video = wordpress.wpgd.getVideo(vid)
    sources = wordpress.wpgd.getVideoSources(vid)
    base_url = current_app.config['BASE_URL']
    base_url = base_url if base_url[-1:] != '/' else base_url[:-1] #corta a barra final
    video_sources = []
    for s in sources:
        print s['format'], s['format'][0:s['format'].find(';')]
        f = s['format'][0:s['format'].find(';')]
        video_sources.append("<source type=\"%s\" src=\"%s\">" % ( f, s['url'] ))
    return render_template('video.html', video=video, sources=video_sources
        ,menu=wordpress.exapi.getMenuItens(menu_slug='menu-principal')
        ,base_url=base_url)


@videos.route('/embed/<int:vid>/')
def embed(vid):
    video = wordpress.wpgd.getVideo(vid)
    sources = wordpress.wpgd.getVideoSources(vid)
    return render_template('videoembed.html', video=video, sources=sources)
