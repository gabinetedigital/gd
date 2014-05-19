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
from flask import Blueprint, url_for, session, request, redirect, make_response, render_template, flash
from flask_oauth import OAuth #, OAuthException
from gd.auth.forms import SignupForm, ProfileForm #, ChangePasswordForm

from gd import conf
from gd import auth
from gd.content.wp import wordpress
from gd.utils.gdcache import fromcache, tocache


#Login Cidadao
cidadao = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static')

lc = OAuth().remote_app('lc',
    # base_url='http://meu.hml.procergs.reders/',
    base_url='https://meu.rs.gov.br/',
    request_token_url=None,
    access_token_url='/oauth/v2/token',
    access_token_method='GET',
    access_token_params={'scope': 'id username full_name name email city', 'response_type': 'code', 'grant_type': 'authorization_code'},
    request_token_params={'scope': 'id username full_name name email city', 'response_type': 'code', 'grant_type': 'authorization_code'},
    authorize_url='/oauth/v2/auth',
    consumer_key=conf.LC_APP_ID,
    consumer_secret=conf.LC_APP_SECRET,
)


@cidadao.route('/')
def auth_index():
    return redirect(url_for('.login'))

@cidadao.route('/login/')
def login():
    """Entry point for the facebook login feature"""
    next_url = request.values.get('next') or request.referrer or None
    return lc.authorize(callback=url_for('.lc_authorized',next=next_url, _external=True))


@cidadao.route('/logout/')
def logout():
    next_url = request.values.get('next') or request.referrer or "/"
    auth.logout()
    return redirect( next_url )

@cidadao.route('/data')
def data():
    print "RETUNING USER DATA >>>>>>>>>>>"
    return str(lc.get('/api/v1/person', data={"access_token" : session.get('access_token')[0] }).data)


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
    print "========>>>>> access_token"
    session['access_token'] = (resp['access_token'], '')

    # Let's log the user in if he/she has already signed up.
    userdata = lc.get('/api/v1/person', data={"access_token" : resp['access_token'] } )

    username = userdata.data['username']
    print "LOGANDO VIA LOGIN CIDADAO:", username
    try:
        auth.login(username, "", userdata.data, resp['access_token'], resp['refresh_token'])
        print "LOGIN CIDADAO LOGADO (by email)!"

    except auth.UserUncomplete:
        flash(u"Seu cadastro foi efetuado. Complete agora seu perfil!")
        session['uncomplete_profile'] = True
        return redirect(url_for('auth.profile'))

    except auth.UserNotFound:
        print "NAO ENCONTRADO COM EMAIL, CADASTRANDO..."
        # resp = make_response( redirect(url_for('auth.signup')) )
        # resp.set_cookie('connect_type', 'social_f')
        return redirect(url_for('auth.signup'))

    # resp = make_response( redirect(url_for('index')) )
    # resp.set_cookie('connect_type', 'social_f')
    return redirect( request.args['next'] )


@lc.tokengetter
def get_access_token():
    """Function responsible for getting the facebook token"""
    print "RETURNING TOKEN", session.get('access_token')
    return session.get('access_token')



@cidadao.route('/profile/')
def profile():
    """Shows the user profile form"""

    if not auth.is_authenticated():
        return redirect(url_for('index'))

    template = 'profile.html'
    form = None
    tos = None
    rm = None

    data = auth.authenticated_user().metadata()
    print "DATA FOR PROFILE", data

    # if 'uncomplete_profile' in session:
    #     profile = social(SignupForm, default=data)
    #     # template = "signup-second.html"
    #     # form = social(SignupForm)
    #     tos = fromcache('tossigin') or tocache('tossigin',wordpress.getPageByPath('tos'))
    #     rm = fromcache('moresigin') or tocache('moresigin',wordpress.getPageByPath('signup-read-more'))
    #     del session['uncomplete_profile']
    # else:
    #     profile = social(ProfileForm, default=data)
    profile = social(ProfileForm, default=data)

    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    return render_template(
        template, profile=profile, sidebar=wordpress.getSidebar, menu=menus,
        username=session.get('username'), tos=tos, readmore=rm)


@cidadao.route('/profile_json', methods=('POST',))
def profile_json():
    """Validate the request of the update of a profile.

    This method will not operate in any user instance but the
    authenticated one. If there's nobody authenticated, there's no way
    to execute it successfuly.
    """
    form = social(ProfileForm, False)
    if not form.validate_on_submit():
        # This field is special, it must be validated before anything. If it
        # doesn't work, the action must be aborted.
        if not form.csrf_is_valid:
            return msg.error(_('Invalid csrf token'), 'InvalidCsrfToken')

        # Usual validation error
        return utils.format_csrf_error(form, form.errors, 'ValidationError')

    # Let's save the authenticated user's meta data
    mget = form.meta.get
    try:
        user = auth.authenticated_user()
    except auth.NobodyHome:
        return redirect(url_for('index'))

    # First, the specific ones
    email = mget('email')
    user.name = mget('name')
    user.receive_sms = mget('receive_sms')
    user.receive_email = mget('receive_email')
    user.email = email

    # Saving the thumbnail
    form.meta.pop('avatar')
    if bool(form.avatar.file):
        flike = form.avatar.file
        thumb = utils.thumbnail(flike, (48, 48))
        form.meta['avatar'] = Upload.imageset.save(
            FileStorage(thumb, flike.filename, flike.name),
            'thumbs/%s' % user.name[0].lower())

    # And then, the meta ones, stored in `UserMeta'
    for key, val in form.meta.items():
        user.set_meta(key, val)

    # return msg.ok({
    #     'data': _('User profile updated successfuly'),
    #     'csrf': form.csrf.data,
    # })
    flash(_(u'Profile update successful'), 'alert-success')
    return redirect(url_for('.profile'))


def social(form, show=True, default=None):
    """This function prepares a signup form to be used from a social
    network.

    This version is currently LoginCidadao only, but it's easy to extend it
    to support other social networks."""
    # Here's the line that says that we're social or not
    #
    data = default or {}
    # data.update(facebook or twitter)
    inst = form(**data) if show else form()
    inst.csrf_enabled = False

    # Preparing form meta data
    inst.social = True


    if default and 'social' in default:
        inst.social = default['social']

    inst.meta = inst.data.copy()

    # Cleaning unwanted metafields (they are not important after
    # validating the form)
    if 'csrf' in inst.meta:
        del inst.meta['csrf']
    if 'accept_tos' in inst.meta:
        del inst.meta['accept_tos']

    # Setting up meta extra fields
    inst.meta['lc'] = session.get('username')


    inst.meta['fromsocial'] = True
    # inst.meta['password'] = urandom(10)
    # else:
    #     print "IS NOT FACEBOOK OR TWITTER!"

    # We're not social right now
    return inst
