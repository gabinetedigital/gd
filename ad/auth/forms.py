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

from ad.utils import _
from ad.auth import choices
from flaskext.wtf import validators
from flaskext.wtf import Form, TextField, PasswordField, SelectField, \
    BooleanField


class SignupForm(Form):
    """Wtform that builds the signup form"""

    name = TextField(
        _('Name'),
        [validators.Length(min=5)],
    )

    email = TextField(
        _('Email'),
        [validators.Email(message=_(u'That\'s not a valid email address.')),
        ]
    )

    email_confirmation = TextField(
        _('Email confirrmation'),
        [validators.Email(message=_(u'That\'s not a valid email address.')),
        ]
    )

    password = PasswordField(
        _('Password'),
    )

    password_confirmation = PasswordField(
        _('Password confirmation'),
    )

    country = SelectField(
        _('Country'),
        choices=choices.COUNTRIES,
        default=u'Brasil',
    )

    state = SelectField(
        _('State'),
        choices=choices.STATES,
        default='RS',
    )

    city = SelectField(
        _('City'),
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

    accept_tos = BooleanField(
        _('Have you read and accepted our <a href="%s">Terms of use</a>?' %
          #FIXME: We don't have this url defined yet
          #url_for('content.page', name='tos'))
          ''),
    )
