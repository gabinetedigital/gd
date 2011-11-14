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

from flask import Blueprint, request, render_template
from gd.content.wp import wordpress
from gd.utils import msg, format_csrf_error, format_csrf_error
from gd import auth
from gd.govpergunta.forms import ContribForm
from gd.model import Contrib, session


govpergunta = Blueprint(
    'govpergunta', __name__,
    template_folder='templates',
    static_folder='static')


@govpergunta.route('/')
def index():
    """Renders the index template"""
    form = ContribForm()
    return render_template('govpergunta.html', wp=wordpress, form=form)

@govpergunta.route('/vote')
def vote():
    """Renders the index template"""
    form = ContribForm()
    return render_template('vote.html')


@govpergunta.route('/contrib_json', methods=('POST',))
def contrib_json():
    """Receives a user contribution and saves to the database

    This function will return a JSON format with the result of the
    operation. That can be successful or an error, if it finds any
    problem in data received or the lack of the authentication.
    """
    if not auth.is_authenticated():
        return msg.error(_(u'User not authenticated'))

    form = ContribForm(csrf_enabled=False)
    if form.validate_on_submit():
        Contrib(
            title=form.data['title'],
            content=form.data['content'],
            theme=form.data['theme'],
            user=auth.authenticated_user())
        session.commit()

        # Returning the csrf
        data = { 'data': _('Contribution received successful') }
        data.update({ 'csrf': form.csrf.data })
        return msg.ok(data)
    else:
        return format_csrf_error(form, form.errors, 'ValidationError')
