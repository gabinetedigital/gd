# Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
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
from gd.content.wp import wordpress


class QuestionForm(Form):
    """Form that receives questions from users to the "Answer" tool"""

    theme = SelectField(
        _('Theme'),
        [validators.Required(
                message=_(u'You need to choose one of the options above'))],
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

    question = TextField(
        _('Content'),
        [validators.Length(
                min=5,
                message=_(u'Your contribution is too short! It needs to have '
                          u'at least 50 chars')
                ),
         ],
    )

