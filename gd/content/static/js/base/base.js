$(function(){
    $('.hide').hide();


    $('.busca').focusin(function(){
        $(".busca").switchClass( "input-small", "input-big", 300 );
        return false;
    });

    $('.busca').focusout(function(){
        $(".busca").switchClass( "input-big", "input-small", 300 );
        return false;
    });

    $('#menu a[href^="#"]').not('.carousel-control').bind('click.smoothscroll',function (e) {
        e.preventDefault();
        var target = this.hash,
        $target = $(target);
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 500, 'swing', function () {
            window.location.hash = target;
        });
    });


    // $(".scroll").scrollable({ circular: true }).autoscroll({ autoplay: true }).click(function() {
    //     $(this).data("scrollable").next();
    // });


    $('#menu').each(function () {
        var $spy = $(this).scrollspy('refresh')
    });

    //$('.on').hide();
    // $('.logado').hide();

    $('.entrar').click(function(){
        $('.off').hide();
        $('.on').fadeIn();
    });

    // $('.form-inline').click(function(){
    //     $('.off').hide();
    //     $('.on').hide();
    //     $('.logado').fadeIn();
    // });


    //Executa esta funcionalida depois de 400ms por causa dos scripts dos vídeos se tiver na capa, pois
    //eles demoram um pouco para redimensionar o video, e se não estiver pronto, o masonry nao funciona direito.
    window.setTimeout(function() {
        var $container = $('.thumbnails');
        $container.imagesLoaded( function(){
            $container.masonry({
                itemSelector : '.thumbnails>li',
                columnWidth: function( containerWidth ) {
                    //console.log(containerWidth / 12);
                    return containerWidth / 12;
                }
            });
            $('.thumbnails').masonry('reload');
        });
    }, 1500);

    // //Auth functions
    // function handleBeforeSubmit(form) {
    //     $('span.loginmsg').fadeOut();
    //     return true;
    // }

    // handleSuccess = function(form, data) {
    //     var errors = data.msg.data;
    //     var code = data.code;
    //     var csrfToken = data.msg.csrf;

    //     /* It's everything ok, let's get out */
    //     $('span.loginmsg').html(data.msg);
    //     if (data.status === 'ok') {
    //         $('span.loginmsg').addClass('alert-success');
    //         auth.userAuthenticated(data.msg.user);
    //         $('span.loginmsg').fadeIn();
    //     } else {
    //         $('span.loginmsg').addClass('alert-error');
    //         $('span.loginmsg').fadeIn();
    //     }

    //     window.setTimeout(function(){
    //         $('span.loginmsg').fadeOut();
    //     },5000);
    // }

    // $('#frmLogin').ajaxForm({
    //     dataType: 'json',

    //     beforeSubmit: function () { handleBeforeSubmit($('#frmLogin')); },
    //     success: function (data) { handleSuccess($('#frmLogin'), data); }
    // });


    // $('#remember_password').ajaxForm({
    //     dataType: 'json',
    //     beforeSubmit: function () { handleBeforeSubmit($('#frmLogin')); },
    //     success: function (data) { handleSuccess($('#frmLogin'), data); }
    // });

    // // $('span#loginmsg').hide();
    // // $('.passwordReminder').hide();
    // // $('#signupoverlay').hide();
    // // $('#tos').hide();

    // auth.callback_login = function(action){
    //     // alert('callback:' + action);
    //     console.log('callback do login:' + action);
    //     if( $('#iframevotacao') ){
    //         var ifr = $('#iframevotacao')[0];
    //         try{
    //             console.log('iframe');
    //             if(ifr.contentWindow){
    //                 if(action == 'login'){
    //                     url = VOTACAO_ROOT + "/visit/?email=" + auth.user.email + "&callback=" + VOTACAO_URL;
    //                     console.log(auth.user);
    //                     ifr.src = url;
    //                 }
    //                 if(action == 'logout'){
    //                     url = VOTACAO_ROOT + "/unvisit/?callback=" + VOTACAO_URL;
    //                     ifr.src = url;
    //                 }
    //                 console.log(url);
    //             }
    //         }catch(erro){ }
    //     }
    // };

//    documentin = "localhost";

    _verifica_pode_adicionar_idea = function(){
        return auth.isAuthenticated();
    }

    _chama_tela_login = function(){
        alert('É necessário estar logado para poder contribuir.');
        scroll(0,0);
        auth.showLoginForm();
    }

    //Controle sinistro do menu! Utilizando o atributo data-link.
    $('a[data-link]').unbind("click").click(function(event){
        event.preventDefault();
        document.location = $(this).attr('data-link');
    });

    $('div.tweets li').popover();

});

// $(document).ready(function(){
//     if(TWITTER_HASH_TAG_CABECALHO){
//         // $.getJSON("http://search.twitter.com/search.json?rpp=25&callback=?&q=" + TWITTER_HASH_TAG_CABECALHO,function(data){
//         $.getJSON("https://api.twitter.com/1.1/search/tweets.json?result_type=mixed&count=4&q=" + TWITTER_HASH_TAG_CABECALHO,function(data){
//             for(var i=0; i < 25 && i < data.results.length; i++){
//                 option = {
//                     title: '@'+data.results[i].from_user_name,
//                     content: data.results[i].text,
//                     trigger: 'hover',
//                     placement: 'left'
//                 };
//                 var number = 1 + Math.floor(Math.random() * 8);
//                 $('.tweets ul').prepend("<li class='pessoa"+number+"' id='"+i+"'> </li>");
//                 $('.tweets li').popover(option);
//             }
//         });
//     }
// });

// Metodo para exibir o contador de carcteres restantes para os comentarios
// Uso: <textarea maxlength="500" onKeyUp="countChar(this,500,'#contador')"></textarea>
function countChar(obj, total_bytes, id_contador) {
    var len = obj.value.length;
    if (len > total_bytes) {
      obj.value = obj.value.substring(0, total_bytes);
      return false;
  } else {
      $(id_contador).text(total_bytes - len);
  }
};

// OVERWRITES old selecor
jQuery.expr[':'].contains = function(a, i, m) {
  return jQuery(a).text().toUpperCase()
      .indexOf(m[3].toUpperCase()) >= 0;
};

function _clearFileInput(oldInput){
    // var oldInput = document.getElementById("fileInput");

    var newInput = document.createElement("input");

    newInput.type = "file";
    newInput.id = oldInput.id;
    newInput.name = oldInput.name;
    newInput.className = oldInput.className;
    newInput.style.cssText = oldInput.style.cssText;
    // copy any other relevant attributes

    oldInput.parentNode.replaceChild(newInput, oldInput);
}

// Method for clear all fields in a form element
jQuery.fn.clearFields = function(){

    form = $(this);

    if(form.prop('tagName') != "FORM")
        return;

    form.find(':input').each(function() {
        switch(this.type) {
            case 'file':
                _clearFileInput(this);
                break;
            case 'password':
            case 'select-multiple':
            case 'select-one':
            case 'text':
            case 'textarea':
                $(this).val('');
                break;
            case 'checkbox':
            case 'radio':
                this.checked = false;
        }
    });
};

jQuery.fn.animateAuto = function(prop, speed, callback){
    var elem, height, width;
    return this.each(function(i, el){
        el = jQuery(el), elem = el.clone().css({"height":"auto","width":"auto"}).appendTo("body");
        height = elem.css("height"),
        width = elem.css("width"),
        elem.remove();

        if(prop === "height")
            el.animate({"height":height}, speed, callback);
        else if(prop === "width")
            el.animate({"width":width}, speed, callback);
        else if(prop === "both")
            el.animate({"width":width,"height":height}, speed, callback);
    });
}
