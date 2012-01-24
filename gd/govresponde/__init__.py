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
    ctx['wordpress'] = wordpress
    ctx['theme'] = theme_id and govr.getTheme(theme_id) or ''
    if auth.is_authenticated():
        ctx['userstats'] = govr.getUserStats(auth.authenticated_user().id)
    ctx.update(custom or {})
    return ctx


@govresponde.route('/')
def index():
    contribs = []

    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    contribs_raw, count = wordpress.govr.getContribs(
        '', user_id, 0, 'date', '', '', 'responded')
    for i in contribs_raw[::-1]:
        contrib = i
        contrib['created_at'] = dateparser.parse(contrib['created_at'])
        contribs.append(contrib)

    ctx = _get_context({ 'contribs': contribs, 'count': count })
    return render_template(
        'govresponde_edicoesanteriores.html', **ctx)


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
        '',                     # sortby
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
        question = i
        question['created_at'] = dateparser.parse(question['created_at'])
        questions.append(question)

    ctx.update({ 'questions': questions, 'pagination': pagination })
    return render_template('govresponde_questions.html', **ctx)


@govresponde.route('/questions/<int:qid>')
def question(qid):
    if wordpress.govr.contribIsAggregated(qid):
        abort(404)

    # Looking for the authenticated user
    user_id = auth.is_authenticated() and \
        auth.authenticated_user().id or ''

    # Small fix for the date value in the question content
    contrib = wordpress.govr.getContrib(qid, user_id)
    contrib['created_at'] = dateparser.parse(contrib['created_at'])

    return render_template(
        'govresponde_question.html',
        **_get_context({ 'question': contrib })
    )


@govresponde.route('/vote/<int:qid>')
def vote(qid):
    return str(wordpress.govr.contribVote(
        qid, auth.authenticated_user().id))
