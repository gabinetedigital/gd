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
from flask import Blueprint, url_for, session, request, redirect, make_response
from flask_oauth import OAuth #, OAuthException

from gd import conf
from gd import auth


cidadao = Blueprint('logincidadao', __name__,
    template_folder='templates',
    static_folder='static')

lc = OAuth().remote_app('lc',
    base_url='http://meu.hml.procergs.reders/',
    request_token_url=None,
    access_token_url='/oauth/v2/token',
    authorize_url='/oauth/v2/auth',
    consumer_key=conf.LC_APP_ID,
    consumer_secret=conf.LC_APP_SECRET,
    request_token_params={'scope': 'id,username,full_name,name,cpf,birthdate,email,city'}
)


@cidadao.route('/')
def auth_index():
    return redirect(url_for('.login'))

@cidadao.route('/login')
def login():
    """Entry point for the facebook login feature"""
    next_url = request.values.get('next') or request.referrer or None
    return lc.authorize(callback=conf.BASE_URL+url_for('.lc_authorized',
        next=next_url, _external=True))


@cidadao.route('/data')
def data():
    return str(lc.get('/api/v1/person').data)


@cidadao.route('/authorized')
@lc.authorized_handler
def lc_authorized(resp):
    """Callback that is fired by login cidadao after user acceptance"""
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.values['error_reason'],
            request.values['error_description']
        )

    # This is the flag that says that a user is logged in from a social
    # network!
    print "========>>>>> OAUTH_TOKEN"
    session['oauth_token'] = (resp['access_token'], '')

    # Let's log the user in if he/she has already signed up.
    userdata = lc.get('/api/v1/person')

    username = userdata.data['email']
    print "LOGANDO VIA FACE:", username
    try:
        auth.login(username, None, fromsocial=True)
        print "FACE LOGADO!"
    except auth.UserNotFound:
        print "NAO LOGADO, CADASTRANDO..."
        resp = make_response( redirect(url_for('auth.signup')) )
        resp.set_cookie('connect_type', 'social_f')
        return resp

    resp = make_response( redirect(url_for('index')) )
    resp.set_cookie('connect_type', 'social_f')
    return resp


@lc.tokengetter
def get_facebook_oauth_token():
    """Function responsible for getting the facebook token"""
    return session.get('oauth_token')


# def checkfblogin():
#     try:
#         if request.cookies.get('connect_type') == 'social_f':
#             req = lc.get('/me')
#             print "\n\nFACEBOOK DATA FROM USER /me =================================="
#             print req.data
#         else:
#             return {}
#     except :
#         return {}

#     if 'error' in req.data or not 'oauth_token' in session:
#         return {}

#     # The following data will be used to fill a part of the signup form
#     # in the first user's login.
#     user = req.data

#     print "\n\n ======================================= FACEBOOK DATA ==================================="
#     print user
#     print " ======================================= FACEBOOK DATA ===================================\n\n"

#     location = user['location']['name'].split(', ', 1) + ['']
#     states = dict((x[1], x[0]) for x in auth.choices.FULL_STATES)
#     city, state = city, state = location[:2]
#     gender = user.get('gender') and user['gender'][0] or None
#     link = user['link']
#     return {
#         'id': user['id'],
#         'name': user['name'],
#         'email': user['email'],
#         'email_confirmation': user['email'],
#         'gender': gender,
#         'facebook': link[link.rindex('/')+1:],
#         # 'city': city,
#         # 'state': states.get(state),
#     }
