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

"""Module that uses the Template and Model APIs to build the Audience web
interface.
"""

from flask import Blueprint, render_template, request
from gd.model import Audience, Term, get_or_404
from gd.utils import dumps
from sqlalchemy.orm.exc import NoResultFound
from gd.content.wp import wordpress

audience = Blueprint(
    'audience', __name__,
    template_folder='templates',
    static_folder='static')


@audience.route('/<int:aid>')
def index(aid):
    """Renders an audience with its public template"""
    inst = get_or_404(Audience, id=aid, visible=True)
    how_to = wordpress.getPageByPath('how-to-use-governo-escuta')
    return render_template(
        'audience.html',
        audience=inst,
        how_to=getattr(how_to, 'content', ''),
        notice=inst.get_last_published_notice(),
    )


@audience.route('/<int:aid>/public_buzz')
def public_buzz(aid):
    """Returns the public buzz of an audience in JSON format"""
    return dumps([buzz.to_dict(deep={ 'type_': {} })
                  for buzz in Audience.query.get(aid).get_public_buzz()])


@audience.route('/<int:aid>/moderated_buzz')
def moderated_buzz(aid):
    """Returns the moderated buzz of an audience in JSON format"""
    return dumps([buzz.to_dict(deep={ 'type_': {} })
                  for buzz in Audience.query.get(aid).get_moderated_buzz()])
