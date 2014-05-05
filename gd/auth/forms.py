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

"""This module holds the declaration of all forms used by the auth app
"""

from gd.utils import phpass
from gd.auth import choices, authenticated_user
from gd.model import Upload

from flask.ext.wtf import validators, ValidationError
from flask.ext.wtf import Form, TextField, PasswordField, SelectField, \
    BooleanField, FileField, file_allowed


class BaseDataForm(Form):
    """Form that holds fields used by more forms bellow"""

    name = TextField(
        _('Name'),
        # [validators.Length(min=5)],
    )

    email = TextField(
        _('Email'),
        [validators.Email(message=_(u'That\'s not a valid email address.')),
        ]
    )

    state = SelectField(
        _('State'),
        # [validators.Required()],
        choices=choices.STATES,
        default='RS',
    )

    city = SelectField(
        _('City'),
        # [validators.Required()],
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

    phone = TextField(
        _('Phone'),
    )

    facebook = TextField(
        _('Facebook'),
    )

    twitter = TextField(
        _('Twitter'),
    )


    receive_email = BooleanField(
        _('I want to receive updates by email.'),
        default=True,
    )

    receive_sms = BooleanField(
        _('I want to receive updates by sms.'),
        default=False,
    )

    # def validate_receive_sms(self, field):
    #     print "VALIDANDO RECEBIMENTO DE SMS com ou sem telefone!!!!", field.data, self.phone.data
    #     """Validate if cel-phone number is present"""
    #     if ( (field.data in ['Y','y'] or field.data == True) and not self.phone.data):
    #         raise ValidationError(
    #             _(u'Cel phone number is required'))


    # def validate_email_confirmation(self, field):
    #     """Compound validation between email and its confirmation"""
    #     if field.data != self.email.data:
    #         raise ValidationError(
    #             _(u'Email does not match its confirmation'))


    def validate_phone(self, field):
        if self.receive_sms:
            if self.receive_sms.data and not field.data:
                raise ValidationError(
                    _(u'This field is required.'))




class SignupForm(BaseDataForm):
    """Wtform that builds the signup form"""

    # email_confirmation = TextField(
    #     _('Email confirmation'),
    #     [validators.Email(message=_(u'That\'s not a valid email address.')),
    #     ]
    # )

    accept_tos = BooleanField(
        _('Have you read and accepted our '
          '<a href="javascript:auth.toggleSignupTab(\'tos\')">'
          'Terms of use</a>?'),
        [validators.Required(),],
        default=True,
    )

    receive_email = BooleanField(
        _('I want to receive updates by email.'),
        default=True,
    )

    receive_sms = BooleanField(
        _('I want to receive updates by sms.'),
        default=False,
    )

    # def validate_receive_sms(self, field):
    #     print "VALIDANDO RECEBIMENTO DE SMS com ou sem telefone!!!!", field.data, self.phone.data
    #     """Validate if cel-phone number is present"""
    #     if ( (field.data in ['Y','y'] or field.data == True) and not self.phone.data):
    #         raise ValidationError(
    #             _(u'Cel phone number is required'))


    # def validate_email_confirmation(self, field):
    #     """Compound validation between email and its confirmation"""
    #     if field.data != self.email.data:
    #         raise ValidationError(
    #             _(u'Email does not match its confirmation'))


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

