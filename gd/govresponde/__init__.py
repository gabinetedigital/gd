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

from flask import Blueprint, request, render_template, redirect, url_for
from dateutil import parser as dateparser

from gd import auth
from gd.utils import msg, format_csrf_error
from gd.content import wordpress
from gd.govresponde import forms

govresponde = Blueprint(
    'govresponde', __name__,
    template_folder='templates',
    static_folder='static')


def _get_theme():
    theme_id = request.values.get('theme')
    return theme_id and wordpress.govr.getTheme(theme_id) or None


@govresponde.route('/')
def index():
    return render_template(
        'govresponde_edicoesanteriores.html',
        wordpress=wordpress)


@govresponde.route('/send')
def send():
    form = forms.QuestionForm(csrf_enabled=False)
    form.theme.choices = [(None, '----')] + \
        [(i['id'], i['name']) for i in wordpress.govr.getThemes()]

    return render_template(
        'govresponde_enviar.html',
        wordpress=wordpress, form=form)


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
    theme = _get_theme()
    questions = []
    questions_raw, count = wordpress.govr.getVotingContribs(
        theme and theme['id'] or '', # theme id
        0,                           # page number
        '',                          # sortby
        '',                          # from
        '',                          # to
    )
    for i in questions_raw:
        question = i.copy()
        question['created_at'] = dateparser.parse(question['created_at'])
        questions.append(question)
    return render_template(
        'govresponde_questions.html',
        wordpress=wordpress, theme=_get_theme(),
        questions=questions, count=count)


@govresponde.route('/vote/<int:qid>')
def vote(qid):
    return str(wordpress.govr.contribVote(
        qid, auth.authenticated_user().id))
