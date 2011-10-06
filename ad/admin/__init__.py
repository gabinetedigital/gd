# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
#   Author: Rodrigo Sebastiao da Rosa <rodrigo-rosa@procergs.rs.gov.br>
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

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import desc, not_
from ad.model import Audience, Buzz, Term, session
from ad.utils import _, msg

admin = Blueprint(
    'admin', __name__,
    template_folder='templates',
    static_folder='static')


@admin.route('/')
def index():
    """A temporary empty view"""
    return 'Please access the /audience url in your browser!'


@admin.route('/audience')
def audiences():
    """Main view, lists all registered audiencces"""
    return render_template('admin/listing.html', title=_(u'Audience'),
                           audience=Audience)


@admin.route('/audience/new', methods=('GET', 'POST'))
def new():
    """Shows the form that creates new audiences and save collected data
    in the database.
    """
    if request.method == 'POST':
        inst = Audience()
        inst.title = request.form['title']
        inst.subject = request.form['subject']
        inst.description = request.form['description']
        inst.embed = request.form['embed']
        inst.visible = request.form['visible']
        terms = request.form.getlist('term')
        main = request.form['main']
        for term in terms:
            newterm = Term(hashtag=term, main=(main==term))
            inst.terms.append(newterm)
        
        inst.owner = 'Admin'
        session.commit()

        return render_template(
            'admin/listing.html', title=_(u'Audience'),
            audience=Audience)
    
    return render_template('admin/new.html', title=_(u'Audience'))


@admin.route('/audience/<int:aid>', methods=('GET', 'POST'))
def edit(aid):
    """Returns a form to edit an audience and saves new params in the
    database.
    """
    inst = Audience.query.get(aid)
    if request.method == 'POST':
        inst.title = request.form['title']
        inst.subject = request.form['subject']
        inst.description = request.form['description']
        inst.embed = request.form['embed']
        inst.visible = request.form['visible']
        
        # deleting all terms
        term = Term.query.filter_by(audience=inst)
        term.delete()

        # adding new terms defined by the user
        terms = request.form.getlist('term')
        main = request.form['main']
        for term in terms:
            newterm = Term(hashtag=term, main=(main==term))
            inst.terms.append(newterm)

        # temporary owner for all objects created in the admin
        # interface.
        inst.owner = 'Admin'

        session.commit()
        return redirect(url_for('.audiences'))

    return render_template(
        'admin/edit.html', title=_(u'Audience'), inst=inst)


@admin.route('/audience/<int:aid>/delete', methods=['GET', 'POST'])
def remove(aid):
    """Delete an audience instance and its related terms in the
    database."""
    audience = Audience.query.get(aid)
    term = Term.query.filter_by(audience=audience)
    term.delete()
    audience.delete()
    session.commit()
    return redirect(url_for('.audiences'))


@admin.route('/audience/<int:aid>/moderate')
def moderate(aid):
    """Returns a list of buzzes for moderation."""
    audience = Audience.query.get(aid)
    status = Buzz.status.in_([u'inserted']) \
        if request.values.get('status', 'new') == 'new' \
        else not_(Buzz.status.in_([u'inserted']))
    buzz_list = Buzz.query \
        .filter_by(audience=audience) \
        .filter(status) \
        .order_by(desc('creation_date'))
    return render_template(
        'admin/moderate.html', audience=audience, buzz_list=buzz_list)


@admin.route('/audience/batch', methods=('post',))
def batch():
    """Batch processing a list of buzz notices"""
    action = request.form['action']
    notices = Buzz.query.filter(Buzz.id.in_(request.form.getlist('notice')))
    { 'accept': lambda: [setattr(i, 'status', u'approved') for i in notices],
      'remove': lambda: [i.delete() for i in notices],
      'suggest': lambda: [setattr(i, 'status', u'selected') for i in notices],
    }[action]()
    session.commit()
    return msg.ok('Notices processed: %s' % action)


@admin.route('/buzz/<int:bid>/accept')
def accept(bid):
    """Approve messages to appear in the main buzz area"""
    buzz = Buzz.query.get(bid)
    buzz.status = u'approved'
    session.commit()
    return msg.ok('Buzz accepted')


@admin.route('/buzz/<int:bid>/delete')
def delete_buzz(bid):
    """Delete Buzz"""
    Buzz.query.get(bid).delete()
    session.commit()
    return msg.ok('Buzz deleted successfuly')
