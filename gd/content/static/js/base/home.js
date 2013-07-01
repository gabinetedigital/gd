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

    $('.botaovotacapa').hover(function(){
        $(this).find('button').removeClass('btn-primary');
        $(this).find('button').addClass('btn-success');
    },function(){
        $(this).find('button').removeClass('btn-success');
        $(this).find('button').addClass('btn-primary');
    })

    $('#frmquestao1').find('button').click(function(){
        // console.log('Gravando...' + $(this).attr('data-value') );
        $('#frmquestao1').find('input[name=hdnquestao1]').val( $(this).attr('data-value') );
    })

    $('#frmquestao1').ajaxForm({
        success: function(pData){
            console.log(pData);
            if(pData.status == 'ok'){
                $('#frmquestao1').find('button').addClass('disabled').attr('disabled','disabled');
                $('.questao2').fadeIn(function(){
                     $('html, body').animate({
                         scrollTop: $("#titquestao2").offset().top - 50
                     }, 600);
                });
            }else{
                alert(pData.msg);
            }
        }
    });    

});

var donextstep = function(op){
    $('#frmquestao1').find('button').addClass('disabled').attr('disabled','disabled');
    $('#botao'+op).removeClass('btn-primary').addClass('btn-success');
    $('.questao2').show();
};
