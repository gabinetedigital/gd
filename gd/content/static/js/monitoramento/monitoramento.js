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

    $('.comofunciona').mouseover(function(){
        $(".comofunciona > .content > .more").fadeOut();
        $(".comofunciona").animate({
            height: "350px",
        }, 500 );
    });

    $('.comofunciona').mouseleave(function(){
        $(".comofunciona").animate({
            height: "60px",
        }, 500 );
        $(".comofunciona > .content > .more").fadeIn();
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

    $(".botoesparticipar a").fancybox({
        afterLoad  : function(current, previous){
            // console.log(window.location);
            console.log(current.content);
            // console.log(current.group[0]);
            if (!auth.isAuthenticated()){
                // alert("Você não está logado!");
                var lnk = "/auth/login?next="+window.location.pathname;
                current.content = "<div class='alert alert-error alert-block'><h4>É necessário efetuar login para participar</h4><br><div style='text-align:center;'><a href='"+lnk+"' class='btn btn-success'>Entrar</a></div></div>";
                // window.setTimeout(function(){
                //     window.location.href=lnk;
                // },2000) ;
                // return false;
            }
        },
        beforeShow  : function(){
            $("#part-texto").clearFields();
            $("#part-imagem").clearFields();
            $("#part-video").clearFields();
            $(".alert.message").hide();
        },
        openEffect  : 'elastic',
        closeEffect : 'elastic',
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
    $('#part-texto').ajaxForm({
        success:ret
    });
    $('#part-video').ajaxForm({
        success:ret
    });
    $('#part-imagem').ajaxForm({
        success:ret
    });

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
        $('.follow').hide();
        $(this.target).show();
        $(this.target).find('input[type=submit]').removeAttr('disabled');
        $(this.target).find('input[type=submit]').addClass('btn-success');
        $(this.target).find("input[type=text]").focus();
        return false;
    });
});
