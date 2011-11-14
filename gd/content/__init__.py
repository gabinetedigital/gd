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

"""Module that instantiates our Flask WSGI app and associates all
implemented blueprints in various modules to this app.
"""

import gettext
import xmlrpclib
from flask import Flask, request, render_template, session, \
     redirect, url_for

from gd import conf
from gd.auth import is_authenticated, authenticated_user, NobodyHome
from gd.content.wp import wordpress
from gd.utils import dumps, msg
from gd.model import session as dbsession
from gd.model import get_mayor_last_tweet, User

from gd.auth.webapp import auth
from gd.auth.fbauth import fbauth
from gd.govpergunta import govpergunta
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(fbauth, url_prefix='/auth/fb')
app.register_blueprint(govpergunta, url_prefix='/govpergunta')

# Registering a secret key to be able to work with sessions
app.secret_key = conf.SECRET_KEY

# Loading the config variables from our `gd.conf' module
app.config.from_object(conf)

# Gettext setup
app.jinja_env = app.jinja_env.overlay(extensions=['jinja2.ext.i18n'])
app.jinja_env.install_gettext_callables(
    gettext.gettext, gettext.ngettext, newstyle=True)


@app.context_processor
def extend_context():
    """This function is a context processor. It injects variables such
    as `user' and `host' variable in all templates that will be rendered
    for this application"""

    context = {}

    # This will be used to bind socket.io client API to our
    # server. Without the port information.
    context['host'] = request.host.split(':')[0]

    # It's also useful to be able to access the configuration module
    # from some templates
    context['conf'] = conf

    # Time to add the `user' var
    try:
        context['user'] = authenticated_user()
    except NobodyHome:
        context['user'] = None

    # Job done!
    return context


@app.after_request
def cleanup(response):
    """Closes the database session that will be open once again in the
    next request"""
    dbsession.close()
    return response


# --- Static special pages ---


@app.route('/')
def index():
    """Renders the index template"""
    slideshow = wordpress.getRecentPosts(
        category_name='highlights',
        post_status='publish',
        numberposts=4,
        thumbsizes=['slideshow'])

    news = wordpress.getRecentPosts(
        category_name='news',
        post_status='publish',
        numberposts=2,
        thumbsizes=['newsbox', 'widenewsbox'])

    return render_template(
        'index.html', wp=wordpress,
        slideshow=slideshow, news=news,
        last_tweet=get_mayor_last_tweet(),
        videos=wordpress.wpgd.getHighlightedVideos(2),
    )


@app.route('/sobre')
def sobre():
    """Renders the about template"""
    return render_template(
        'about.html', page=wordpress.getPageByPath('about'))


@app.route('/teaser')
def teaser():
    """Renders the teaser template"""
    return render_template('teaser.html')


@app.route('/govescuta')
def govescuta():
    """Renders the teaser template"""
    return render_template('govescuta.html')


@app.route('/gallery')
def gallery():
    return render_template('galeria.html')

#this is not currently used!
@app.route('/confirm_signup/<string:key>', methods=('GET',))
def confirm_signup(key):
    try:
        user = User.query.filter_by(user_activation_key=key).one()
        user.user_activation_key = ''
        dbsession.commit()
    except NoResultFound:
        return home_page(dumps({'error':_(u'Authorization key not found in the database. Perhaps your profile is already enabled!')}))
    except:
        return home_page(dumps({'error':_(u'There was an error processing the request')}))
    return home_page(dumps({'username':user.username,'message':_('Your profile was enabled successfully')}))


@app.route('/news')
@app.route('/news/<int:page>')
def news(page=0):
    """List posts in chronological order"""
    pagination, posts = wordpress.getPosts(page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        posts=posts)


@app.route('/cat/<int:cid>')
@app.route('/cat/<int:cid>/<int:page>')
def category(cid, page=0):
    """List posts of a given category"""
    pagination, posts = wordpress.getPostsByCategory(cat=cid, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        posts=posts)


@app.route('/tag/<string:slug>')
@app.route('/tag/<string:slug>/<int:page>')
def tag(slug, page=0):
    """List posts of a given tag"""
    pagination, posts = wordpress.getPostsByTag(tag=slug, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        posts=posts)


def post_page(pid, error_msg=''):
    """A generic function that renders a post template"""
    recent_posts = wordpress.getRecentPosts(
        post_status='publish',
        numberposts=4)
    return render_template(
        'post.html',
        post=wordpress.getPost(pid),
        tags=wordpress.getTagCloud(),
        sidebar=wordpress.getSidebar,
        comments=wordpress.getComments(post_id=pid),
        error_msg=error_msg,
        show_comment_form=is_authenticated(),
        recent_posts=recent_posts)


@app.route('/pages/<path>')
def pages(path):
    """Renders a wordpress page"""
    return render_template(
        'page.html',
        page=wordpress.getPageByPath(path),
        sidebar=wordpress.getSidebar,
    )


@app.route('/pages/<path:path>.json')
def page_json(path):
    """Returns a page data in the JSON format"""
    page = wordpress.getPageByPath(path)
    return dumps(page and page.data or None)


@app.route('/post/<int:pid>')
def post(pid):
    """View that proxies the `post_page' function"""
    return post_page(pid)


@app.route('/new_comment', methods=('POST',))
def new_comment():
    """Posts new comments to the blog"""
    if not is_authenticated():
        return msg.error(_(u'User not authenticated'))
    try:
        wordpress.newComment(
            username=session['username'],
            password=session['password'],
            post_id=request.form['post_id'],
            content=request.form['content']
        )
        return msg.ok(_(u'Thank you. Your comment was successfuly sent'))
    except xmlrpclib.Fault, err:
        return msg.error(_(unicode(err.faultString)), code='CommentError')


@app.route('/search/<string:s>')
@app.route('/search/<string:s>/<int:page>')
def search(s, page=0):
    """Renders the search template"""
    pagination, posts = wordpress.search(s=s, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getSidebar,
        pagination=pagination,
        search_term=s,
        posts=posts)


@app.route('/feed')
def feed():
    """Renders the RSS wordpress function"""
    header = {'Content-Type': 'application/rss+xml; charset=utf-8'}
    return wordpress.getRSS(), 200, header
