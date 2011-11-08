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
from gd.model import session as dbsession
from gd.utils import dumps

from gd.admin import admin
from gd.audience import audience
from gd.auth.fbauth import fbauth
from gd.auth.webapp import auth
from gd.buzz.webapp import buzz
from gd.buzz.facebookapp import fbapp
from gd.govpergunta import govpergunta
from gd.model import get_mayor_last_tweet

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(buzz, url_prefix='/buzz')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(fbauth, url_prefix='/auth/fb')
app.register_blueprint(audience, url_prefix='/audience')
app.register_blueprint(fbapp, url_prefix='/fbapp')
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


@app.route('/')
def teaser():
    """Renders the teaser template"""
    return render_template('teaser.html')


@app.route('/sobre')
def sobre():
    """Renders the about template"""
    return render_template(
        'about.html', page=wordpress.getPageByPath('about'))


@app.route('/news')
@app.route('/news/<int:page>')
def news(page=0):
    """List posts in chronological order"""
    pagination, posts = wordpress.getPosts(page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getMainSidebar(),
        pagination=pagination,
        posts=posts)


@app.route('/home')
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


@app.route('/cat/<int:cid>')
@app.route('/cat/<int:cid>/<int:page>')
def category(cid, page=0):
    """List posts of a given category"""
    pagination, posts = wordpress.getPostsByCategory(cat=cid, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getMainSidebar(),
        pagination=pagination,
        posts=posts)


@app.route('/tag/<string:slug>')
@app.route('/tag/<string:slug>/<int:page>')
def tag(slug, page=0):
    """List posts of a given tag"""
    pagination, posts = wordpress.getPostsByTag(tag=slug, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getMainSidebar(),
        pagination=pagination,
        posts=posts)

@app.route('/pages/<path>')
def pages(path):
    """Renders a wordpress page"""
    return render_template(
        'page.html',
        page=wordpress.getPageByPath(path),
        sidebar=wordpress.getMainSidebar(),
    )


@app.route('/pages/<path:path>.json')
def page_json(path):
    """Returns a page data in the JSON format"""
    page = wordpress.getPageByPath(path)
    return dumps(page and page.data or None)


def post_page(pid, error_msg=''):
    """A generic function that renders a post template"""
    recent_posts = wordpress.getRecentPosts(
        post_status='publish',
        numberposts=4)
    return render_template(
        'post.html',
        post=wordpress.getPost(pid),
        tags=wordpress.getTagCloud(),
        sidebar=wordpress.getMainSidebar(),
        comments=wordpress.getComments(post_id=pid),
        error_msg=error_msg,
        show_comment_form=is_authenticated(),
        recent_posts=recent_posts)


@app.route('/post/<int:pid>')
def post(pid):
    """View that proxies the `post_page' function"""
    return post_page(pid)


@app.route('/new_comment', methods=('POST',))
def new_comment():
    """Posts new comments to the blog"""
    if not is_authenticated():
        return post_page(request.form['post_id'])
    try:
        wordpress.newComment(
            username=session['username'],
            password=session['password'],
            post_id=request.form['post_id'],
            content=request.form['content']
        )
        return redirect(url_for('post', pid=request.form['post_id']))
    except xmlrpclib.Fault, err:
        return post_page(request.form['post_id'], err.faultString)


@app.route('/search/<string:s>')
@app.route('/search/<string:s>/<int:page>')
def search(s, page=0):
    """Renders the search template"""
    pagination, posts = wordpress.search(s=s, page=page)
    return render_template(
        'archive.html',
        sidebar=wordpress.getMainSidebar(),
        pagination=pagination,
        search_term=s,
        posts=posts)

@app.route('/feed')
def feed():
    header = {'Content-Type': 'application/rss+xml; charset=utf-8'}
    return wordpress.getRSS(), 200, header
