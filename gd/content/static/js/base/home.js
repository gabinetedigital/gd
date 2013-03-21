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

    $('.go1').click(function(){
        $('.step1').fadeIn();
        $('.step2').hide();
        $('.step3').hide();
        $('.step4').hide();
        $('.go1 a').addClass('active');
        $('.go4 a').removeClass('active');
        $('.go2 a').removeClass('active');
        $('.go3 a').removeClass('active');
    });

    $('.go2').click(function(){
        $('.step2').fadeIn();
        $('.step1').hide();
        $('.step3').hide();
        $('.step4').hide();
        $('.go2 a').addClass('active');
        $('.go1 a').removeClass('active');
        $('.go4 a').removeClass('active');
        $('.go3 a').removeClass('active');
    });

    $('.go3').click(function(){
        $('.step3').fadeIn();
        $('.step2').hide();
        $('.step1').hide();
        $('.step4').hide();
        $('.go3 a').addClass('active');
        $('.go1 a').removeClass('active');
        $('.go2 a').removeClass('active');
        $('.go4 a').removeClass('active');
    });

    $('.go4').click(function(){
        $('.step4').fadeIn();
        $('.step2').hide();
        $('.step3').hide();
        $('.step1').hide();
        $('.go4 a').addClass('active');
        $('.go1 a').removeClass('active');
        $('.go2 a').removeClass('active');
        $('.go3 a').removeClass('active');
    });

    $('#myTab a:last').tab('show');

    $('div#clipping-itemsclipping').easyPaginate({
        step:$('#clipping-perpage').val()
    });

    var totequipe_grupo = document.getElementById('equipe-perpage').value;
    for(i=2;i<=totequipe_grupo;i++){
        $('#equipe-grupo-'+i).hide();
    }

    $('.clipping').hide();
    $('.publicacoes').hide();

    $('.clip').click(function(){
        $('.equipe').hide();
        $('.publicacoes').hide();
        $('.clipping').fadeIn();
        $('.thumbnails').masonry('reload');
    });

    $('.membros').click(function(){
        $('.clipping').hide();
        $('.publicacoes').hide();
        $('.equipe').fadeIn();
        $('.thumbnails').masonry('reload');
    });

    $('.pub').click(function(){
        $('.clipping').hide();
        $('.equipe').hide();
        $('.publicacoes').fadeIn();
        $('.thumbnails').masonry('reload');
    });

    $('.equipe-grupo-1').addClass('active');

    $('.subgrupo button').click(function(){
        for(i=1;i<=totequipe_grupo;i++){
            $('#equipe-grupo-'+i).hide();
        }
        $('.equipe-grupo').removeClass('active');
        $('#equipe-grupo-'+$(this).attr('data-index')).fadeIn();
        $('.thumbnails').masonry('reload');
        $('.equipe-grupo-'+$(this).attr('data-index')).addClass('active');
    });

});
