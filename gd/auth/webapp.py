#! -*- encoding: utf8 -*-
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

"""Web application definitions for the `auth' module"""

from os import urandom
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, render_template, request, session, make_response, flash, redirect
from werkzeug import FileStorage

from gd import utils
from gd import conf
from gd.utils import msg
from gd import auth as authapi
from gd.auth.fbauth import checkfblogin, facebook as remote_facebook
from gd.auth import forms
from gd.model import Upload, session as dbsession, User
from gd.content.wp import wordpress
from gd.utils.gdcache import fromcache, tocache


auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static')


def social(form, show=True, default=None):
    """This function prepares a signup form to be used from a social
    network.

    This version is currently facebook only, but it's easy to extend it
    to support other social networks."""
    # Here's the line that says that we're social or not
    #
    # FIXME: Debug and discover why this damn facebook stuff does not
    # work properly.
    facebook = checkfblogin() or {}
    #facebook = {}
    data = default or {}
    data.update(facebook)
    inst = form(**data) if show else form()
    inst.csrf_enabled = False

    # Preparing form meta data
    inst.social = bool(facebook)
    if default and 'social' in default:
        inst.social = default['social']
    inst.meta = inst.data.copy()

    # Cleaning unwanted metafields (they are not important after
    # validating the form)
    if 'csrf' in inst.meta:
        del inst.meta['csrf']
    if 'accept_tos' in inst.meta:
        del inst.meta['accept_tos']
    if 'password_confirmation' in inst.meta:
        del inst.meta['password_confirmation']

    if facebook:
        print "REMOVING PASSWORD for FACEBOOK LOGIN"
        # Removing the password field. It's not needed by a social login
        if 'password' in inst: del inst.password
        if 'password_confirmation' in inst: del inst.password_confirmation

        # Setting up meta extra fields
        inst.meta['fbid'] = facebook['id']
        inst.meta['fromsocial'] = True
        inst.meta['password'] = urandom(10)
    else:
        print "IS NOT FACEBOOK!"

    # We're not social right now
    return inst


@auth.route('/login/')
def login_form():
    """Renders the login form"""
    formcad = social(forms.SignupForm)
    next = request.args.get('next') or request.referrer
    return render_template('login.html', form=formcad, next=next)


@auth.route('/lost_password/')
def lost_password():
    """Renders the lost password form"""
    return render_template('lost_password.html')


@auth.route('/logon', methods=('POST',))
def logon():
    """Logs the user in and returns the user object in
    JSON format"""
    username = request.values.get('username')
    password = request.values.get('password')
    gonext = True
    if username and password:
        try:
            user = authapi.login(username, password)
        except authapi.UserNotFound:
            flash(_(u'Wrong user or password'), 'alert-error')
            gonext = False
        except authapi.UserAndPasswordMissmatch:
            flash(_(u'Wrong user or password'), 'alert-error')
            gonext = False
        # else:
            # msg.ok({ 'user': user })
            # flash(_(u'Login successfuly!'), 'alert-success')
    else:
        flash(_(u'Username or password missing'), 'alert-error')
        gonext = False
    formcad = social(forms.SignupForm)

    next = request.values.get('next',default="")
    if next is not None and gonext:
        return redirect(next)
    else:
        if request.referrer:
            return redirect(request.referrer)
        else:
            return render_template('login.html', form=formcad)


@auth.route('/logout/')
def logout():
    """Logs the user out and returns """
    authapi.logout()
    next = request.values.get('next')
    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    try:
        twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
    except KeyError:
        twitter_hash_cabecalho = ""

    if next:
        print "NEXTT=", next
        return redirect(next)
    else:
        return render_template('logout.html',
            menu=menus,
            twitter_hash_cabecalho=twitter_hash_cabecalho
            )

@auth.route('/logout_json')
def logout_json():
    """Logs the user out and returns an ok message"""
    authapi.logout()

    resp = make_response( msg.ok(_(u'User loged out')) )
    resp.set_cookie('connect_type', '')
    return resp
    # return msg.ok(_(u'User loged out'))


@auth.route('/signup')
def signup_form():
    """Renders the signup form"""

    default_data=None
    print session.keys()
    if request.cookies.get('connect_type') == 'social_f':
        f_data=remote_facebook.get('/me').data
        default_data = {
            'gender': f_data['gender'][:1], #'m' e 'f'
            'name': f_data['name'],
            'email': f_data['email'],
            'email_confirmation': f_data['email'],
            'social': True
        }
        print  "DEFAULT DATA FORM ::::::::::::::::: ", default_data
    else:
        print "NAO TEM FACEBOOK_DATA !!!!!!"

    form = social(forms.SignupForm)
    if 'readmore' in request.args:
        return render_template(
            'signup.html', form=form,
            readmore=wordpress.getPageByPath('signup-read-more'),
        )
    elif 'tos' in request.args:
        return render_template(
            'signup.html', form=form,
            tos=wordpress.getPageByPath('tos'),
        )
    else:
        return render_template(
            'signup.html', form=form,
        )



@auth.route('/signup_json', methods=('POST',))
def signup_json():
    """Register a new user that sent his/her informations through the
    signup form"""
    form = social(forms.SignupForm, False)
    fromsocial = request.cookies.get('connect_type') == 'social_f'

    # Proceeding with the validation of the user fields
    form.fromsocial = fromsocial
    if form.validate_on_submit():
        try:
            meta = form.meta
            dget = meta.pop
            if fromsocial:
                password = ""
            else:
                password = dget('password')

            # Finally, it's time to create the user
            user = authapi.create_user(
                dget('name'), dget('email'), password,
                dget('email_confirmation'), form.meta,
                dget('receive_sms'), dget('receive_email') )
            utils.send_welcome_email(user)
        except authapi.UserExists:
            return utils.format_csrf_error(
                form, _(u'User already exists'), 'UserExists')
        except authapi.EmailAddressExists:
            return utils.format_csrf_error(
                form,
                _(u'The email address informed is being used '
                  u'by another person'), 'EmailAddressExists')
        utils.send_welcome_email(user)
        return msg.ok({})
    else:
        return utils.format_csrf_error(form, form.errors, 'ValidationError')


@auth.route('/profile/')
def profile_form():
    """Shows the user profile form"""
    data = authapi.authenticated_user().metadata()
    profile = social(forms.ProfileForm, default=data)
    passwd = forms.ChangePasswordForm()
    menus = fromcache('menuprincipal') or tocache('menuprincipal', wordpress.exapi.getMenuItens(menu_slug='menu-principal') )
    try:
        twitter_hash_cabecalho = conf.TWITTER_HASH_CABECALHO
    except KeyError:
        twitter_hash_cabecalho = ""
    return render_template(
        'profile.html', profile=profile, passwd=passwd, menu=menus, twitter_hash_cabecalho=twitter_hash_cabecalho)


@auth.route('/profile_json', methods=('POST',))
def profile_json():
    """Validate the request of the update of a profile.

    This method will not operate in any user instance but the
    authenticated one. If there's nobody authenticated, there's no way
    to execute it successfuly.
    """
    form = social(forms.ProfileForm, False)
    if not form.validate_on_submit():
        # This field is special, it must be validated before anything. If it
        # doesn't work, the action must be aborted.
        if not form.csrf_is_valid:
            return msg.error(_('Invalid csrf token'), 'InvalidCsrfToken')

        # Usual validation error
        return utils.format_csrf_error(form, form.errors, 'ValidationError')

    # Let's save the authenticated user's meta data
    mget = form.meta.get
    user = authapi.authenticated_user()

    # First, the specific ones
    user.name = mget('name')
    user.email = mget('email')

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

    return msg.ok({
        'data': _('User profile updated successfuly'),
        'csrf': form.csrf.data,
    })


@auth.route('/profile_passwd_json', methods=('POST',))
def profile_passwd_json():
    """Update the user password"""
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        user = authapi.authenticated_user()
        user.set_password(form.password.data)
        dbsession.commit()
        return msg.ok({
            'data': _('Password updated successful'),
            'csrf': form.csrf.data,
        })
    else:
        # This field is special, it must be validated before anything. If it
        # doesn't work, the action must be aborted.
        if not form.csrf_is_valid:
            return msg.error(_('Invalid csrf token'), 'InvalidCsrfToken')

        # Usual validation error
        return utils.format_csrf_error(form, form.errors, 'ValidationError')


@auth.route('/remember_password', methods=('POST',))
def remember_password():
    """An HTTP view that answers requests for a new password"""
    try:
        user = User.query.filter_by(email=request.values['email']).one()
        new_pass = utils.generate_random_password()
        if utils.send_password(request.values['email'], new_pass):
            user.set_password(new_pass)
            dbsession.commit()
        else:
            dbsession.rollback()
            raise Exception('Unable to send the email')
    except NoResultFound:
        flash( _(u'E-mail not found in the database'), 'alert-error' )
    except Exception, exc:
        flash( _(u'There was an error sending the e-mail'), 'alert-error' )
    else:
        flash(_('Password sent to the email'), 'alert-success')
    return render_template('lost_password.html')
