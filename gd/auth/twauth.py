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

"""Authentication machinery for facebook"""

# from httplib2 import ServerNotFoundError
from flask import Blueprint, url_for, session, request, redirect, make_response, flash
from flask_oauth import OAuth, OAuthException

from gd import conf
from gd import auth


twauth = Blueprint('twauth', __name__)

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key='qlAIf5O55R5ZQwZeJZVzA',
    consumer_secret='8OGDeR9CsEGWNfBJuqUdPvufCMfZG7SEwNAKoySct4'
)


@twauth.route('/')
def login():
    """Entry point for the facebook login feature"""
    next_url = request.values.get('next') or request.referrer or None
    print "TWITTER LOGIN BEGIN", conf.BASE_URL+url_for(
            '.twitter_authorized'), next_url
    return twitter.authorize(callback=conf.BASE_URL+url_for(
            '.twitter_authorized', next=next_url))


# @twauth.errorhandler(OAuthException)
# def handle_oauth_exception(error):
#     print "ERROR NO LOGIN DO TWITTER!", error
#     flash(str(error), 'alert-error')
#     return redirect(url_for('auth.login'))


@twauth.route('/data')
def data():
    return str(twitter.get('users/show.json',screen_name=session['tmp_twitter_id']).data)


@twauth.route('/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    """Callback that is fired by twitter after user acceptance"""
    print "@twitter.authorized_handler <<<<=========="
    next_url = request.args.get('next') or url_for('auth.login')
    if resp is None:
        print "NAO <<<<=========="
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    print 'RESP=======>', dir(resp), resp
    # This is the flag that says that a user is logged in from a social
    # network!
    print "========>>>>> OAUTH_TOKEN TWITTER"
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    # Let's log the user in if he/she has already signed up.
    # userdata = twitter.get('/me')

    username = resp['screen_name']
    print "LOGANDO VIA TWITTER:", username
    try:
        auth.login(username, None, fromsocial=True)
        print "TWITTER LOGADO!"
    except auth.UserNotFound:
        print "NAO LOGADO, CADASTRANDO TWITTER..."
        session['tmp_twitter_id'] = username
        resp = make_response( redirect(url_for('auth.signup')) )
        resp.set_cookie('connect_type', 'social_t')
        return resp

    resp = make_response( redirect(url_for('index')) )
    resp.set_cookie('connect_type', 'social_t')
    return resp


@twitter.tokengetter
def get_twitter_oauth_token(token=None):
    """Function responsible for getting the twitter token"""
    print "::GET TWITTER TOKEN::", token, session.get('twitter_token')
    return session.get('twitter_token') or None


def checktwlogin():
    try:
        print "checktwlogin::CONNECT_TYPE", request.cookies.get('connect_type')
        if request.cookies.get('connect_type') == 'social_t':
            print "REQUESTING USER INFORMATION", dir(twitter)
            req = twitter.get('users/show.json',
                data={
                    'screen_name':session['tmp_twitter_id']
                }
            )
            # req = {'id':session['tmp_twitter_id']}
        else:
            return {}
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst
        return {}

    if 'error' in req.data or not 'twitter_token' in session:
        return {}

    # The following data will be used to fill a part of the signup form
    # in the first user's login.
    # print "REQ:", dir(req)
    # print "REQ.DATA:", dir(req.data)
    print "REQ.DATA:", req.data
    # user = req.data
    return {
        'id': req.data['screen_name'],
        'twitter': req.data['screen_name'],
        'name': req.data['name'],
    }
