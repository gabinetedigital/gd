/* Copyright (C) 2012  Guilherme Guerra <guerrinha@comum.org>
 * Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
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

$(document).ready(function () {

    $('#pq').hide();
    $('#pro').hide();
    $('#como').hide();

    $('.prioridade').click(function(){
        $('#pq').hide();
        $('#pro').hide();
        $('#como').hide();
        $('#pri').fadeIn();
    });

    $('.porque').click(function(){
        $('#pri').hide();
        $('#pro').hide();
        $('#como').hide();
        $('#pq').fadeIn();
    });

    $('.processo').click(function(){
        $('#pq').hide();
        $('#pri').hide();
        $('#como').hide();
        $('#pro').fadeIn();
    });

    $('.comofunciona').click(function(){
        $('#pq').hide();
        $('#pro').hide();
        $('#pri').hide();
        $('#como').fadeIn();
    });

    $('div#clipping-itemsclipping').easyPaginate({
        step:document.getElementById('clipping-perpage').value
    });

    var totequipe_grupo = document.getElementById('equipe-perpage').value;
    for(i=2;i<=totequipe_grupo;i++){
        $('#equipe-grupo-'+i).hide();
    }

    $('.equipe-grupo').click(function(){
        for(i=1;i<=totequipe_grupo;i++){
            $('#equipe-grupo-'+i).hide();
        }
        $('#equipe-grupo-'+$(this).attr('data-index')).fadeIn();
    });

});
