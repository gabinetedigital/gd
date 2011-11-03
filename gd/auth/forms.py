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

from gd.utils import phpass, _
from gd.auth import choices, authenticated_user
from gd.model import Upload

from flaskext.wtf import validators, ValidationError
from flaskext.wtf import Form, TextField, PasswordField, SelectField, \
    BooleanField, FileField, file_allowed


class BaseDataForm(Form):
    """Form that holds fields used by more forms bellow"""

    name = TextField(
        _('Name'),
        [validators.Length(min=5)],
    )

    email = TextField(
        _('Email'),
        [validators.Email(message=_(u'That\'s not a valid email address.')),
        ]
    )

    country = SelectField(
        _('Country'),
        [validators.Required()],
        choices=choices.COUNTRIES,
        default=u'Brasil',
    )

    state = SelectField(
        _('State'),
        [validators.Required()],
        choices=choices.STATES,
        default='RS',
    )

    city = SelectField(
        _('City'),
        [validators.Required()],
        choices=choices.CITIES,
        default=u'Porto Alegre',
    )

    age_group = SelectField(
        _('Age group'),
        choices=choices.AGE,
    )

    gender = SelectField(
        _('Gender'),
        choices=choices.GENDER,
    )

    income_group = SelectField(
        _('Income group'),
        choices=choices.INCOME,
    )

    twitter = TextField(
        _('Twitter'),
    )

    facebook = TextField(
        _('Facebook'),
    )


class BasePasswordForm(Form):
    """Form that holds password fields"""

    password = PasswordField(
        _('Password'),
        [validators.Required(),
         ]
    )

    password_confirmation = PasswordField(
        _('Password confirmation'),
        [validators.Required(),
         ]
    )

    def validate_password_confirmation(self, field):
        """Compound validation between password and its confirmation"""
        if field.data != self.password.data:
            raise ValidationError(
                _(u'Password does not match its confirmation'))


class SignupForm(BaseDataForm, BasePasswordForm):
    """Wtform that builds the signup form"""

    email_confirmation = TextField(
        _('Email confirrmation'),
        [validators.Email(message=_(u'That\'s not a valid email address.')),
        ]
    )

    accept_tos = BooleanField(
        _('Have you read and accepted our <a href="%s">Terms of use</a>?' %
          #FIXME: We don't have this url defined yet
          #url_for('content.page', name='tos'))
          ''),
        [validators.Required(),
         ]
    )

    def validate_email_confirmation(self, field):
        """Compound validation between email and its confirmation"""
        if field.data != self.email.data:
            raise ValidationError(
                _(u'Email does not match its confirmation'))


class ProfileForm(BaseDataForm):
    """Wtform that allows the user to change his/her profile"""

    avatar = FileField(
        _('User avatar'),
        validators=[
            file_allowed(
                Upload.imageset,
                _('Only images are allowed in this field!')),
        ]
    )


class ChangePasswordForm(BasePasswordForm):
    """Form to change the password of an user"""

    current_password = PasswordField(
        _('Your current password'),
        [validators.Required(),
         ]
    )

    def validate_current_password(self, field):
        """Validates the current password of the logged in user"""
        hasher = phpass.PasswordHash(8, True)
        user = authenticated_user()
        if not hasher.check_password(field.data, user.password):
            raise ValidationError(
                _('The current password is wrong'))
