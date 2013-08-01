/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

$window.load((function() {
    //Dos videos em destaque
    $('.carousel').carousel();

    $('.searcher').typeahead({
        source: [{%for t in titulos%}'{{t}}',{%endfor%}],
        items: 8,
        minLength: 2,
        updater: function(item){
            //Slugs é um dicionáraio que contém como chave o Título do vídeo, e como valor o id,
            //para poder recdirecionar diretamente para a galeria.
            ids = { {%for t in titulos%}
                    '{{t}}':'{{titulos[t]}}',
                    {%endfor%} }
            document.location = "/videos/" + ids[item]
        }
    });

});
