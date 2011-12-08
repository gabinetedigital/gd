# -*- coding:utf-8 -*-
#
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

"""Web application definitions to the govp tool"""


from json import loads
from flask import Blueprint, request, render_template, redirect, url_for
from flask import session as fsession

from gd import auth
from gd.content.wp import wordpress, gallery
from gd.utils import msg, format_csrf_error, format_csrf_error, dumps
from gd.govpergunta.forms import ContribForm
from gd.model import Contrib, session
from gd.govpergunta.pairwise import Pairwise, InvalidTokenError, \
    PAIRWISE_VERSION

THEMES = {'cuidado': u'Cuidado Integral',
          'familia': u'Saúde da Família',
          'emergencia': u'Urgência e Emergência',
          'medicamentos': u'Acesso a Medicamentos',
          'regional': u'Saúde na sua Região'}

govpergunta = Blueprint(
    'govpergunta', __name__,
    template_folder='templates',
    static_folder='static')


# @govpergunta.route('/contribuir')
# def index():
#     """Renders the index template"""
#     form = ContribForm()
#     return render_template('govpergunta.html', wp=wordpress, form=form)



def _get_pairwise():
    """Helper function to get the pairwise instance saved in the
    session"""
    if ('pairwise' not in fsession) or \
            (fsession['version'] != PAIRWISE_VERSION):
        fsession['pairwise'] = Pairwise()
        fsession['version'] = PAIRWISE_VERSION
    return fsession['pairwise']


@govpergunta.route('/')
def index():
    pairwise = _get_pairwise()
    pair = pairwise.get_pair()
    fsession.modified = True
    return render_template(
        'vote.html',
        pair=pair,
        theme=THEMES[pair['left'].theme]
    )


@govpergunta.route('/results')
def results():
    pagination, posts = wordpress.getPostsByTag(
        tag='governador-perguta')
    images = gallery.search('GovernadorPergunta', limit=3)
    return render_template(
        'results.html', posts=posts, images=images)


@govpergunta.route('/invalidate')
def invalidate():
    """With 50 votes, the user will be redirected to the index page and
    it's pairwise session will be destroied"""
    del fsession['pairwise']
    return redirect(url_for('index'))


@govpergunta.route('/add_vote', methods=('POST',))
def add_vote():
    if ('pairwise' not in fsession) or \
           (fsession['version'] != PAIRWISE_VERSION):
        return redirect(url_for('.index'))

    pairwise = fsession['pairwise']
    try:
        pairwise.vote(
            request.values.get('direction'),
            request.values.get('token'))
        fsession.modified = True
    except InvalidTokenError:
        pass
    return redirect(url_for('.index'))


@govpergunta.route('/contrib_json', methods=('POST',))
def contrib_json():
    """Receives a user contribution and saves to the database

    This function will return a JSON format with the result of the
    operation. That can be successful or an error, if it finds any
    problem in data received or the lack of the authentication.
    """
    if not auth.is_authenticated():
        return msg.error(_(u'User not authenticated'))

    raise Exception('Not funny')

    form = ContribForm(csrf_enabled=False)
    if form.validate_on_submit():
        Contrib(
            title=form.data['title'].encode('utf-8'),
            content=form.data['content'].encode('utf-8'),
            theme=form.data['theme'],
            user=auth.authenticated_user())
        session.commit()

        # Returning the csrf
        data = { 'data': _('Contribution received successful') }
        data.update({ 'csrf': form.csrf.data })
        return msg.ok(data)
    else:
        return format_csrf_error(form, form.errors, 'ValidationError')


# -- JSON API that publishes contributions


def _format_contrib(contrib):
    """Returns a dictionary representation of a contribution"""
    return {
        'id': contrib.id,
        'title': contrib.title,
        'content': contrib.content,
        'creation_date': contrib.creation_date,
        'theme': contrib.theme,
     }


@govpergunta.route('/contribs/all.json')
def contribs_all():
    """Lists all contributions in the JSON format"""
    return dumps([
            _format_contrib(i)
                for i in Contrib.query.filter_by(status=True)])


@govpergunta.route('/contribs/user.json')
def contribs_user():
    """Lists all contributions in the JSON format"""
    try:
        user = auth.authenticated_user()
    except auth.NobodyHome:
        return dumps([])
    return dumps([
            _format_contrib(i)
                for i in Contrib.query
                    .filter_by()
                    .filter(Contrib.user==user)])


@govpergunta.route('/contribs/choosen.json')
def contribs_choosen():
    """Lists all contributions in the JSON format"""
    query = Contrib.query.filter_by(status=True, enabled=True)[:50]
    contribs = {}
    for key in THEMES.keys():
        contribs[key] = []
        for data in wordpress.pairwise.getSortedByScore(0, 10, key)[0]:
            contrib = Contrib.get(loads(data['data'])['id'])
            final = _format_contrib(contrib)
            final['author'] = contrib.user.name

            final['children'] = []
            for subcontrib in contrib.children:
                subfinal = _format_contrib(subcontrib)
                subfinal['author'] = subcontrib.user.name
                final['children'].append(subfinal)

            for subcontrib in Contrib.query.filter_by(parent=contrib.id):
                subfinal = _format_contrib(subcontrib)
                subfinal['author'] = subcontrib.user.name
                final['children'].append(subfinal)
            contribs[key].append(final)
    return dumps(contribs)
