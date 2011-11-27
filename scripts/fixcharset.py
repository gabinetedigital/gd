# -*- coding:utf-8 -*-
#
# Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
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

from gd.model import Contrib, session

erros = 0
bugados = []
for i in range(1, 1000):
    try:
        contrib = Contrib.get(i)
        if contrib is not None:
            print contrib.id
            contrib.title = contrib.title.decode('utf-8')
            contrib.content = contrib.content.decode('utf-8')
            session.commit()
    except Exception, exc:
        session.rollback()
        erros += 1
        bugados.append({ 'id': i, 'exception': exc })

print ('Foram encontrados %d erros, provavelmente esses objetos '
       'já são unicode') % (erros)
print 'Seguem os erros: %s' % (', '.join([str(x['id']) for x in bugados]))
