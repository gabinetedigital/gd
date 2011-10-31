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

from httplib2 import ServerNotFoundError
from flask import Blueprint, url_for, session, request, redirect
from flaskext.oauth import OAuth, OAuthException

from gd import conf
from gd.auth import choices


fbauth = Blueprint('fbauth', __name__)
facebook = OAuth().remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=conf.FACEBOOK_APP_ID,
    consumer_secret=conf.FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_location'}
)


@fbauth.route('/')
def login():
    """Entry point for the facebook login feature"""
    next_url = request.values.get('next') or request.referrer or None
    return facebook.authorize(callback=url_for(
            '.facebook_authorized', next=next_url, _external=True))


@fbauth.route('/data')
def data():
    return str(facebook.get('/me').data)


@fbauth.route('/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    """Callback that is fired by facebook after user acceptance"""
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.values['error_reason'],
            request.values['error_description']
        )

    # This is the flag that says that a user is logged in from a social
    # network!
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    """Function responsible for getting the facebook token"""
    return session.get('oauth_token')


def checkfblogin():
    try:
        req = facebook.get('/me')
    except (ServerNotFoundError, OAuthException):
        return {}

    if 'error' in req.data:
        return {}

    # The following data will be used to fill a part of the signup form
    # in the first user's login.
    user = req.data
    location = user['location']['name'].split(', ', 1) + ['']
    states = dict((x[1], x[0]) for x in choices.FULL_STATES)
    city, state = city, state = location[:2]
    gender = user.get('gender') and user['gender'][0] or None
    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'email_confirmation': user['email'],
        'gender': gender,
        'facebook': user['link'],
        'city': city,
        'state': states.get(state),
    }
