# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
#   Author: Rodrigo Sebastiao da Rosa <rodrigo-rosa@procergs.rs.gov.br>
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
from ad.content.wp import wordpress


content = Blueprint(
    'content', __name__,
    template_folder='templates',
    static_folder='static')


@content.route('/')
def index():
    """Renders the index template"""
    slideshow = wordpress.getRecentPosts(
        category_name='highlights',
        post_status='published',
        numposts=4,
        thumbsizes=['slideshow'])
    news = wordpress.getRecentPosts(
        category_name='news',
        post_status='published',
        numposts=2,
        thumbsizes=['newsbox', 'widenewsbox'])
    return render_template(
        'index.html', wp=wordpress,
        slideshow=slideshow, news=news)
