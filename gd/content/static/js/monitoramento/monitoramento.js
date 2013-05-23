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


    // $(".botoesparticipar a").fancybox({
    //     afterLoad  : function(current, previous){
    //         // console.log(window.location);
    //         console.log(current.content);
    //         // console.log(current.group[0]);
    //         if (!auth.isAuthenticated()){
    //             // alert("Você não está logado!");
    //             var lnk = "/auth/login?next="+window.location.pathname;
    //             current.content = "<div class='alert alert-error alert-block'><h4>É necessário efetuar login para participar</h4><br><div style='text-align:center;'><a href='"+lnk+"' class='btn btn-success'>Entrar</a></div></div>";
    //             // window.setTimeout(function(){
    //             //     window.location.href=lnk;
    //             // },2000) ;
    //             // return false;
    //         }
    //     },
    //     beforeShow  : function(){
    //         $("#part-texto").clearFields();
    //         $("#part-imagem").clearFields();
    //         $("#part-video").clearFields();
    //         $(".alert.message").hide();
    //     },
    //     openEffect  : 'elastic',
    //     closeEffect : 'elastic',
    // });

    var abreAbaixo = function(){

        // A div que vai conter os novos conteudos, no topo da timeline
        var todiv   = $(".suplementar");
        var fromdiv = $( $(this).attr('href') );

        var toheight = fromdiv.css('height').slice(0,-2);
        console.log(toheight);

        if($('.suplementar').css('height')=="0px"){
            todiv.animate({height:toheight},500, function(){
                todiv.html( fromdiv.html() );
            });
        }else{
            todiv.animate({height:0},500,function(){
                todiv.html("");
            });
        }

    };

    fechaSuplementar = function(){
        var todiv   = $(".suplementar");
        todiv.animate({height:0},500,function(){
            todiv.html("");
            todiv.hide();
        });
    }

    var abreProlado = function(){

        // A div que vai conter os novos conteudos, no topo da timeline
        var todiv   = $(".suplementar");
        var fromdiv = $( $(this).attr('href') );

        var toheight = parseInt(fromdiv.css('height').slice(0,-2)) + 80;

        if(!auth.isAuthenticated()){
            toheight = 180;
        }


        if($('.suplementar').css('height')=="0px"){
            todiv.show();
            todiv.animate({height:toheight},500, function(){

            if (!auth.isAuthenticated()){
                var lnk = "/auth/login?next="+window.location.pathname;
                todiv.html("<div class='alert alert-error alert-block'><h4>É necessário efetuar login para participar</h4><br><div style='text-align:center;'><a href='"+lnk+"' class='btn btn-success'>Entrar</a></div></div>");
            }else{

                todiv.html( fromdiv.html() );
                todiv.find($(this).attr('href')).show();
                // fromdiv.show();

                //Seta o ajaxForm somente aqui pois o jQuery COPIA o html para dentro do div, e não
                //o objeto, e perde a configuração se feita antes.
                $('#part-geral').ajaxForm({
                    success:ret
                });

                $("#link").keyup( function() {
                    if ($(this).val()!=""){
                        $('#foto').attr('disabled','disabled');
                    }else{
                        $('#foto').removeAttr('disabled');
                    }
                });

                $("#foto").change( function() {
                    if ($(this).val()!=""){
                        $('#link').attr('disabled','disabled');
                    }else{
                        $('#link').removeAttr('disabled');
                    }
                });

            }

            });
        }else{
            fechaSuplementar();
        }

    };

    $(".botoesparticipar a").click(abreProlado);

    $('.vote a').on("click",function(){
        var url = $(this).attr('href');
        var _clicado_ = $(this)
        _clicado_.attr('disabled','disabled');
        $.get(url, function(data){
            var pData = $.parseJSON(data);
            // console.log(pData.score);
            // console.log(pData);
            _clicado_.parent().find(".score").html(pData.score);
            _clicado_.removeAttr('disabled');
        });

       return false;
    });

});
