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


from flask.ext.wtf import validators #, ValidationError
from flask.ext.wtf import Form, TextField, SelectField


THEMES = (
    (u'cuidado',)*2,
    (u'familia',)*2,
    (u'emergencia',)*2,
    (u'medicamentos',)*2,
    (u'regional',)*2,
)


class ContribForm(Form):
    """Form that receives contributions from users to the "Ask" tool"""

    theme = SelectField(
        _('Theme'),
        [validators.Required(
                message=_(u'You need to choose one of the options above'))],
        choices=THEMES,
    )

    title = TextField(
        _('Contribution title'),
        [validators.Length(
                min=5,
                message=_(u'Your title is too short! It needs to have '
                          u'at least 5 chars')),
         validators.Length(
                max=256,
                message=_(u'Your title is too long! It needs to have '
                          u'at most 256 chars'))
         ],
    )

    content = TextField(
        _('Content'),
        [validators.Length(
                min=50,
                message=_(u'Your contribution is too short! It needs to have '
                          u'at least 50 chars')
                ),
         validators.Length(
                max=600,
                message=_(u'Your contribution is too long! It needs to have '
                          u'at most 600 chars')
                )],
    )
