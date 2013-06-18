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
from flask import Blueprint, render_template, redirect, current_app
from gd.utils.gdcache import cache, fromcache, tocache, removecache

from gd import auth
from gd.content.wp import wordpress #, gallery
from gd.utils import msg, format_csrf_error, dumps, twitts
from gd.govpergunta.forms import ContribForm
from gd.model import Contrib, session
# from gd.govpergunta.pairwise import Pairwise

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



# def _get_pairwise():
#     """Helper function to get the pairwise instance saved in the
#     session"""
#     if ('pairwise' not in fsession) or \
#             (fsession['version'] != PAIRWISE_VERSION):
#         fsession['pairwise'] = Pairwise()
#         fsession['version'] = PAIRWISE_VERSION
#     return fsession['pairwise']


# @govpergunta.route('/')
# def index():
#     pairwise = _get_pairwise()
#     pair = pairwise.get_pair()
#     fsession.modified = True
#     return render_template(
#         'vote.html',
#         pair=pair,
#         theme=THEMES[pair['left'].theme]
#     )


# @govpergunta.route('/invalidate')
# def invalidate():
#     """With 50 votes, the user will be redirected to the index page and
#     it's pairwise session will be destroied"""
#     del fsession['pairwise']
#     return redirect(url_for('index'))


# @govpergunta.route('/add_vote', methods=('POST',))
# def add_vote():
#     if ('pairwise' not in fsession) or \
#            (fsession['version'] != PAIRWISE_VERSION):
#         return redirect(url_for('.index'))

#     pairwise = fsession['pairwise']
#     try:
#         pairwise.vote(
#             request.values.get('direction'),
#             request.values.get('token'))
#         fsession.modified = True
#     except InvalidTokenError:
#         pass
#     return redirect(url_for('.index'))


@govpergunta.route('/')
def index():
    return redirect('/govpergunta/resultados/')
    # pagination, posts = wordpress.getPostsByTag(
    #     tag='governador-pergunta')
    # images = gallery.search('GovernadorPergunta', limit=24)[::-1]
    # videos = [wordpress.wpgd.getVideo(i) for i in (14, 16, 12)]
    # return render_template(
    #     'results.html', posts=posts, images=images, videos=videos)


@govpergunta.route('/resultados/')
@govpergunta.route('/resultados/<int:ano>/')
# @cache.memoize()
def resultados(ano=2012):
    """Renders a wordpress page special"""
    cn = 'results-{0}'.format(ano)
    slideshow = fromcache(cn) or tocache(cn,wordpress.getRecentPosts(
        category_name='destaque-govpergunta-%s' % str(ano),
        post_status='publish',
        numberposts=4,
        thumbsizes=['slideshow']))

    categoria = 'resultados-gov-pergunta-%s' % str(ano)
    retorno = fromcache("contribs-{0}".format(ano)) or \
              tocache("contribs-{0}".format(ano) ,wordpress.wpgovp.getContribuicoes(principal='S',category=categoria))

    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    try:
        twitter_hash_cabecalho = twitts()
    except KeyError:
        twitter_hash_cabecalho = ""

    questions = None
    for q in retorno:
        if isinstance(q, list):
            questions = q
    return render_template(
        'resultados.html',
        menu=menus,
        questions=questions,
        sidebar=wordpress.getSidebar,
        twitter_hash_cabecalho=twitter_hash_cabecalho,
        ano=ano,
        slideshow=slideshow,
        wp=wordpress
    )


@govpergunta.route('/resultados-detalhe/<int:postid>/')
# @cache.memoize()
def resultado_detalhe(postid):
    """Renders a contribution detail"""
    principal = fromcache("res-detalhe-{0}".format(postid)) or \
                tocache("res-detalhe-{0}".format(postid),wordpress.wpgovp.getContribuicoes(principal='S',postID=postid))
    # print "PRINCIPAL +++++++++++++++++++++", principal[1][0]
    retorno = fromcache("contribs-detalhe-{0}".format(postid)) or \
              tocache("contribs-detalhe-{0}".format(postid),wordpress.wpgovp.getContribuicoes(principal='N',postID=postid))
    # print "RETORNO +++++++++++++++++++++", retorno
    comts = fromcache("com-res-detalhe-{0}".format(postid)) or \
            tocache("com-res-detalhe-{0}".format(postid),wordpress.getComments(status='approve',post_id=postid))
    qtd = retorno[0]
    detalhes = retorno[1]
    return render_template(
        'resultados-detalhes.html',
        agregadas=detalhes,
        qtd_agregadas=qtd,
        principal=principal[1][0],
        comments=comts,
        postid=postid
    )


@govpergunta.route('/results/<path:path>')
# @cache.memoize()
def results_page(path):
    page = fromcache("page-{0}".format(path)) or tocache("page-{0}".format(path),wordpress.getPageByPath(path))
    return render_template('results_page.html', page=page)


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
        'moderation': contrib.moderation,
     }


@govpergunta.route('/contribs/all.json')
# @cache.cached()
def contribs_all():
    """Lists all contributions in the JSON format"""
    r = fromcache("contribs_all_") or  tocache("contribs_all_",dumps([
                                        _format_contrib(i)
                                            for i in Contrib.query.filter_by(status=True)]))
    return r


@govpergunta.route('/contribs/user.json')
# @cache.cached()
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
    contribs = {}
    for key in THEMES.keys():
        contribs[key] = {'name': THEMES[key], 'children': []}
        count = 11 if key == 'familia' else 10
        for data in wordpress.pairwise.getSortedByScore(0, count, key)[0]:
            cid = loads(data['data'])['id']

            # This is _nasty_. The team that carried about organizing
            # contribution approved something wrong. Yes, now we have
            # invalid data on our db. This was the better way I figured
            # out to fix it right now, but obviously something better
            # must be done when we have more time.
            if cid == 1213:
                continue
            contrib = Contrib.get(cid)
            final = _format_contrib(contrib)
            final['author'] = contrib.user.name
            final['score'] = data['score']
            final['votes'] = {
                'score': data['score'],
                'total': data['votes'],
                'won': data['won'],
                'lost': data['lost'],
            }

            final['children'] = []
            for subcontrib in contrib.children:
                subfinal = _format_contrib(subcontrib)
                subfinal['author'] = subcontrib.user.name
                final['children'].append(subfinal)

            for subcontrib in Contrib.query.filter_by(parent=contrib.id):
                subfinal = _format_contrib(subcontrib)
                subfinal['author'] = subcontrib.user.name
                final['children'].append(subfinal)
            contribs[key]['children'].append(final)
    return dumps(contribs)


# @govpergunta.route('/contribs/stats.json')
# def contribs_stats():
#     """Lists all contributions in the JSON format"""
#     def hammer_contrib(c):
#         return '"%(name)s","%(email)s","%(city)s","%(phone)s",' + \
#             '"%(title)s","%(theme)s"' % {
#             'theme': c.theme,
#             'name': c.user.name,
#             'email': c.user.email,
#             'city': c.user.get_meta('city'),
#             'phone': c.user.get_meta('phone'),
#             'title': c.title,
#         }
#
#     contribs = ["nome,email,cidade,telefone,titulo,tema"]
#     for key in THEMES.keys():
#         for data in wordpress.pairwise.getSortedByScore(0, 10, key)[0]:
#             contrib = Contrib.get(loads(data['data'])['id'])
#             contribs.append(hammer_contrib(contrib))
#             for subcontrib in contrib.children:
#                 contribs.append(hammer_contrib(subcontrib))
#             for subcontrib in Contrib.query.filter_by(parent=contrib.id):
#                 contribs.append(hammer_contrib(subcontrib))
#     return '\n'.join(contribs)
