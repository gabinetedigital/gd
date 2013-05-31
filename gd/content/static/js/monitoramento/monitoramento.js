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

$(window).load(function () {

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

    $(".seguirobra").fancybox({
        afterLoad: function(){
            $('.main-follow').find("input[type=text]").val("");
            $('.main-follow').find(".alert").hide();
        },
        afterShow: function(){
            $('.main-follow').find('a[target=#follow-facebook]').trigger('click');
        }
    });

    var showMsg = function(status, otherclass){
        // alert(status);
        $(".alert").html(status);
        if(otherclass){
            $(".alert").addClass(otherclass);
        }
        $(".alert").show();

    };

    var ret = function(data) {
      var pData = $.parseJSON(data);

      /* It's everything ok, let's get out */
      if (pData.status === 'ok') {
          showMsg('Obrigado por sua contribuição!','alert-success');
          window.setTimeout(function(){
            $.fancybox.close();
          },1000);
      } else {
          if(pData.status === 'not_logged'){
            showMsg('Usuário não logado.');
          }
          if(pData.status === 'file_not_allowed'){
            showMsg('O arquivo enviado não é permitido. Use apenas arquivos PNG ou JPG.');
          }
          if(pData.status === 'file_not_found'){
            showMsg('Você não anexou a sua foto no envio!');
          }
      }
    };

    var retSeguir = function(data){
        showMsg('Obrigado! Agora você receberá informações sobre esta obra.','alert-success');
        window.setTimeout(function(){
            $.fancybox.close();
        },3000);
    }

    $('#seguirobraform .ajaxform').ajaxForm({
        success:retSeguir,
        beforeSubmit: function (arr, form, options) {
            form.find('input[type=submit]').attr('disabled','disabled');
            form.find('input[type=submit]').removeClass('btn-success');
        }
    });

    $('#seguirobraform a').click(function(){
        // alert('vai abrir ' + this.target );
        $('.main-follow .follow').hide();
        $(this.target).show();
        $(this.target).find('input[type=submit]').removeAttr('disabled');
        $(this.target).find('input[type=submit]').addClass('btn-success');
        $(this.target).find("input[type=text]").focus();
        return false;
    });


    $('.botoesparticipar a').click( function() {
        $('.suplementar').show();
        $('.updates').hide();
    });

    $('.inVideo').click( function() {
        $('.space .video').show();
        $('.space .foto').hide();
        return false;
    });

    $('.inFoto').click( function() {
        $('.space .video').hide();
        $('.space .foto').show();
        return false
    });

    $('#nome').click( function() {
        $('.telefone').fadeIn();
        $('.newPassword').fadeIn();
        return false
    });


    $('.participe a.votar').on("click",function(){
        var url = $(this).attr('href');
        var _clicado_ = $(this)
        _clicado_.attr('disabled','disabled');
        $.get(url, function(data){
            var pData = $.parseJSON(data);
            _clicado_.parent().find(".counter").html(pData.score);
            _clicado_.removeAttr('href');
            _clicado_.find('i').removeClass("icon-star-empty");
            _clicado_.find('i').addClass("icon-star");
        });

       return false;
    });


    $('.timeline').masonry({
        itemSelector: '.update',
        gutterWidth: 60,
    });

    $(".timeline>.update").each(function(){

        var posLeft = $(this).css("left");

        if(posLeft == "0px") {
            $(this).find('.seta').addClass('esquerda');
        } else {
            $(this).addClass('direita');
            $(this).find('.seta').addClass('direita');
        }
    });

});
