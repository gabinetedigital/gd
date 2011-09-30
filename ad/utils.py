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

"""This module holds general useful functions that are too generic to be
placed anywhere else.
"""

from json import dumps as internal_dumps
from datetime import date, datetime

# It's gonna be changed by some gettext function when we start to care
# about translating things
_ = lambda x:x


def _default_handler(value):
    """Handles usually unserializable objects, currently datetime and
    date objects, converting them to an isoformatted string
    """
    if isinstance(value, (date, datetime)):
        return datetime.isoformat(value)


def dumps(obj):
    """Replacement for builtin `json.dumps' that handles usual
    unserializable objects, like `datetime' instances.
    """
    return internal_dumps(obj, default=_default_handler)
