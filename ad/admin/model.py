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

from elixir import *

metadata.bind = "sqlite:///movies.sqlite" # ?????????????
metadata.bind.echo = True

class Audiencia(Entity):
    codigo = Field(Integer, primary_key=True)
    descricao = Field(UnicodeText)
    data = Field()
    hashtag = Field(Unicode(45))
    visivel = Field()
    data_inclusao = Field()
    usuario_inclusao = Field()
    data_alteracao = Field()
    usuario_alteracao = Field()
    
#    def __repr__(self):
#        return '<Audiencia "%s" (%d)>' % (self.descricao, self.data)

class Tema(Entity):
    codigo = Field(Integer, primary_key=True)
    descricao = Field(UnicodeText)
    data_inclusao = Field()
    usuario_inclusao = Field()
    data_alteracao = Field()
    usuario_alteracao = Field()
    audiencia = OneToMany('Audiencia')
    
    
class Streaming(Entity):
    codigo = Field(Integer, primary_key=True)
    descricao = Field(UnicodeText)
    link_fonte = Field(Unicode(150))
    formato = Field(Unicode(200))
    data_inclusao = Field()
    usuario_inclusao = Field()
    data_alteracao = Field()
    usuario_alteracao = Field()
    audiencia = OneToMany('Audiencia')