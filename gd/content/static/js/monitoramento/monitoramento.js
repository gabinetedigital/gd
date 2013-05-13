/* Copyright (C) 2013  Guilherme Guerra <guerrinha@comum.org>
 * Copyright (C) 2013  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Guilherme Guerra <guilherme-guerra@sgg.rs.gov.br>
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

    $('.carousel').carousel();
    $('.toottip').tooltip();

    $('.icon-list').click(function(){
        $('#lista-obras').fadeIn();
    });

    $('.comentar').click(function(){
        $('.comente').fadeIn();
    });

    $('.label-important').click(function(){
        $('#obras').fadeOut();
        $('.voltar').fadeIn();
    });

    $('.voltar').click(function(){
        $('#obras').fadeIn();
        $('.voltar').fadeOut();
    });

    var sticky_participe_offset_top = $('.follows').offset().top;
    var sticky_participe = function(){
        var scroll_top_part = $(window).scrollTop();
        if (scroll_top_part > sticky_participe_offset_top) {
            $('.follows').addClass('follows-fixed');
        } else {
            $('.follows').removeClass('follows-fixed');
        }
    };

    sticky_participe();
    $(window).scroll(function() {
        sticky_participe();
    });

    $(".seguirobra").fancybox();
    $(".botoesparticipar a").fancybox({
        openEffect  : 'elastic',
        closeEffect : 'elastic',
        beforeShow  : function(){
            console.log($(this));
        }
    });


});
