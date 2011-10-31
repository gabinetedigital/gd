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

from flask import Blueprint, render_template, request
from gd.utils import msg, _
from gd.content.wp import wordpress
from gd.auth import forms
from gd.auth.fbauth import checkfblogin
from gd import auth as authapi

auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static')


@auth.route('/login')
def login_form():
    """Renders the login form"""
    return render_template('login.html')


@auth.route('/login_json', methods=('POST',))
def login_json():
    """Logs the user in (through ajax) and returns the user object in
    JSON format"""
    username = request.values.get('username')
    password = request.values.get('password')
    if username and password:
        try:
            user = authapi.login(username, password)
        except authapi.UserNotFound:
            return msg.error(_(u'User does not exist'), 'UserNotFound')
        except authapi.UserAndPasswordMissmatch:
            return msg.error(_(u'User or password mismatch'),
                             'UserAndPasswordMissmatch')
        return msg.ok({ 'user': user })
    return msg.error(_(u'Username or password missing'), 'EmptyFields')


@auth.route('/logout_json')
def logout_json():
    """Logs the user out and returns an ok message"""
    authapi.logout()
    return msg.ok(_(u'User loged out'))


@auth.route('/signup')
def signup_form():
    """Renders the signup form"""
    # The user is trying to authenticate with his/her facebook id
    facebook = checkfblogin() or {}
    form = forms.SignupForm(**facebook)
    return render_template(
        'signup.html', form=form,
        tos=wordpress.getPageByPath('tos'),
        readmore=wordpress.getPageByPath('signup/read-more'),
    )


@auth.route('/signup_json', methods=('POST',))
def signup_json():
    """Register a new user that sent his/her informations through the
    signup form"""
    form = forms.SignupForm()
    def format_error(orig, code):
        """This function wraps an error message and, instead of
        returning the data content, it adds the a new field: a new csrf
        token.

        It's safe to do it here because only people that sent a valid
        csrf token in the first time can get a new one.
        """
        data = { 'data': orig }
        data.update({ 'csrf': form.csrf.data })
        return msg.error(data, code)

    # This field is special, it must be validated before anything. If it
    # doesn't work, the action must be aborted.
    csrf = request.form['csrf']
    if not csrf or not form.csrf.validate(csrf):
        return msg.error(_('Invalid csrf token'), 'InvalidCsrfToken')

    # Proceeding with the validation of the user fields
    if form.validate_on_submit():
        try:
            meta = form.data.copy()
            dget = meta.pop
            password = dget('password')

            # Removing unwanted fields. The others are going to be used
            # as meta fields in the user instance
            for i in 'csrf', 'password_confirmation', 'accept_tos':
                dget(i)

            # Not sure if it's needed, but saving it anyway
            facebook = checkfblogin()
            if facebook:
                meta['fbid'] = facebook['id']

            # Finally, it's time to create the user
            user = authapi.create_user(
                dget('name'), dget('email'), password,
                dget('email_confirmation'), meta)
        except authapi.UserExists:
            return format_error(_(u'User already exists'), 'UserExists')
        except authapi.EmailAddressExists:
            return format_error(_(u'The email address informed is being used '
                                  u'by another person'), 'EmailAddressExists')
        data = authapi.login_user_instance(user, password)
        return msg.ok({ 'user': data })
    else:
        return format_error(form.errors, 'ValidationError')
