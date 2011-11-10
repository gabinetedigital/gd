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


from flaskext.wtf import validators, ValidationError
from flaskext.wtf import Form, TextField, SelectField


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
                min=5, max=256,
                message=_(u'Your title must have between 5 and 256 chars'))],
    )

    content = TextField(
        _('Content'),
        [validators.Length(
                min=100, max=400,
                message=_('Your contribution must have between '
                          '100 and 400 chars')
                )],
    )
