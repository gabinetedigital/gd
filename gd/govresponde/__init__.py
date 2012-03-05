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

"""Web application definitions to the govr tool"""

from flask import Blueprint, request, render_template, redirect, \
    url_for, abort
from dateutil import parser as dateparser
from math import ceil

from gd import auth
from gd.utils import msg, format_csrf_error
from gd.content import wordpress
from gd.govresponde import forms

govresponde = Blueprint(
    'govresponde', __name__,
    template_folder='templates',
    static_folder='static')


CONTRIBS_PER_PAGE = 50

def _get_context(custom=None):
    theme_id = request.values.get('theme')
    govr = wordpress.govr
    ctx = {}

    # Style customization parameters
    ctx['hidesidebar'] = False
    ctx['rclass'] = ''

    # Parameters from wordpress
    ctx['wordpress'] = wordpress
    ctx['theme'] = theme_id and govr.getTheme(theme_id) or ''

    # Info from authenticated users
    if auth.is_authenticated():
        ctx['userstats'] = govr.getUserStats(auth.authenticated_user().id)

    # Update the default values
    ctx.update(custom or {})
    return ctx


def _format_contrib(contrib):
    contrib['created_at'] = dateparser.parse(contrib['created_at'])
    contrib['answered_at'] = dateparser.parse(contrib['answered_at'])
    contrib['theme'] = wordpress.govr.getTheme(contrib['theme_id'])
    contrib['video'] = wordpress.wpgd.getVideo(contrib['data'])
    contrib['video_sources'] = wordpress.wpgd.getVideoSources(contrib['data'])
    return contrib


@govresponde.route('/')
def index():
    # Getting the user id if the user is authenticated
    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    # Querying the contribs ordenated by the answer date
    contribs = []
    contribs_raw, count = wordpress.govr.getContribs(
        '', user_id, 0, '-answerdate', '', '', 'responded')
    for i in contribs_raw:
        contribs.append(_format_contrib(i))

    # Yes, this is a hammer! This date value will be use to know which
    # question should be highlighted.
    #
    # The rule is actually quite simple. We have to aggregate all the
    # contribs that were published in the same day of the last published
    # one.
    base_date = contribs[0]['answered_at'].strftime('%d/%m/%Y')

    return render_template(
        'govresponde_edicoesanteriores.html', **_get_context({
        'contribs': contribs,
        'count': count,
        'base_date': base_date,
    }))


@govresponde.route('/results/<int:rid>')
@govresponde.route('/results/<int:rid>/<int:page>')
def results(rid, page=0):
    """Shows results about a single answer
    """

    # Looking for the authenticated user
    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    # Getting the contrib itself and all its related posts. The page
    # parameter is used to paginate referral query result.
    contrib = _format_contrib(wordpress.govr.getContrib(rid, user_id))
    if contrib['category']:
        pagination, posts = wordpress.getPostsByCategory(
            cat=contrib['category'], page=page)
    else:
        pagination, posts = None, []

    # Building the context to return the template
    return render_template(
        'govresponde_results.html',
        **_get_context({
            'contrib': contrib,
            'hidesidebar': True,
            'rclass': 'result',
            'referrals': posts,
            'pagination': pagination,
        })
    )


@govresponde.route('/comofunciona')
def comofunciona():
    return render_template(
        'govresponde_comofunciona.html',
        **_get_context({
            'page': wordpress.getPageByPath('govresponde/como-funciona'),
        })
    )


@govresponde.route('/send')
def send():
    form = forms.QuestionForm(csrf_enabled=False)
    form.theme.choices = [(None, '----')] + \
        [(i['id'], i['name']) for i in wordpress.govr.getThemes()]

    return render_template(
        'govresponde_enviar.html',
        **_get_context({ 'form': form }))


@govresponde.route('/send_json', methods=('POST',))
def send_json():
    form = forms.QuestionForm(csrf_enabled=False)
    form.theme.choices = [(None, '----')] + \
        [(i['id'], i['name']) for i in wordpress.govr.getThemes()]
    if form.validate_on_submit():
        wordpress.govr.createContrib(
            form.data['title'],
            form.data['theme'],
            form.data['question'],
            auth.authenticated_user().id,
            '', 0, 0
        )
        return msg.ok(u'Contribution received successful')
    else:
        return format_csrf_error(form, form.errors, 'ValidationError')


@govresponde.route('/questions')
def questions():
    ctx = _get_context()
    theme = ctx['theme']
    questions = []
    sortby = request.values.get('sortby', '-date')

    # Looking for the authenticated user
    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    # Discovering the theme id
    theme_id = theme and \
        theme['id'] or ''

    # Finally, listing the questions that are able to receive votes.
    pagination = {}
    pagination['page'] = int(request.values.get('page', 0))
    questions_raw, count = wordpress.govr.getVotingContribs(
        theme_id,               # theme id
        user_id,                # user id
        pagination['page'],     # page number
        sortby,                 # sortby
        '',                     # to
        '',                     # from
        CONTRIBS_PER_PAGE,      # perpage
    )

    # Pagination stuff
    count = int(count)
    pagination['pages'] = int(ceil(float(count) / CONTRIBS_PER_PAGE))
    pagination['count'] = count

    # Small fix for the date value in the question content
    for i in questions_raw:
        question = _format_contrib(i)
        questions.append(question)

    ctx.update({
        'questions': questions,
        'pagination': pagination,
        'sortby': sortby,
    })
    return render_template('govresponde_questions.html', **ctx)


@govresponde.route('/questions/<int:qid>')
def question(qid):
    if wordpress.govr.contribIsAggregated(qid):
        abort(404)

    # Looking for the authenticated user
    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    # Getting the contrib
    contrib = _format_contrib(wordpress.govr.getContrib(qid, user_id))

    # Just making sure that the user is authorized to see the requested
    # contrib
    if contrib['status'] != 'approved':
        abort(404)

    return render_template(
        'govresponde_question.html',
        **_get_context({ 'question': contrib })
    )


@govresponde.route('/vote/<int:qid>')
def vote(qid):
    return str(wordpress.govr.contribVote(
        qid, auth.authenticated_user().id))
