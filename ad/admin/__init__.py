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

"""Module that uses the Template and Model APIs to build the Admin web
interface.
"""

from flask import Blueprint, render_template
from .utils import _

admin = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static')

@admin.route('/')
def index():
    return 'Please access the /audience url in your browser!'

@admin.route('/audience')
def audiences():
    """Main view, lists all registered audiencces"""
    return render_template('admin/listing.html', title=_(u'Audience'))

@admin.route('/audience/new')
def new():
    """Shows the form that creates new audiences and save collected data
    in the database.
    """
    return render_template('admin/new.html', title=_(u'Audience'))

@admin.route('/audience/<int:aid>')
def audience(aid):
    """Returns a form to edit an audience and saves new params in the
    database.
    """
    return render_template('admin/edit.html', title=_(u'Audience'))
