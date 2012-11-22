$(function(){
    var sticky_navigation_offset_top = $('.subnav').offset().top;
    var sticky_navigation = function(){
        var scroll_top = $(window).scrollTop();
        if (scroll_top > sticky_navigation_offset_top) {
            $('.subnav').addClass('subnav-fixed');
        } else {
            $('.subnav').removeClass('subnav-fixed');
        }
    };

    sticky_navigation();
    $(window).scroll(function() {
        sticky_navigation();
    });

    $('.busca').focusin(function(){
        $(".busca").switchClass( "input-small", "input-big", 300 );
        return false;
    });

    $('.busca').focusout(function(){
        $(".busca").switchClass( "input-big", "input-small", 300 );
        return false;
    });

    $('a[href^="#"]').not('.carousel-control').bind('click.smoothscroll',function (e) {
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

    $('.on').hide();
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

    auth.updateLoginWidget();

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

    //Auth functions
    function handleBeforeSubmit(form) {
        $('span#loginmsg').fadeOut();
        return true;
    }

    handleSuccess = function(form, data) {
        var errors = data.msg.data;
        var code = data.code;
        var csrfToken = data.msg.csrf;

        /* It's everything ok, let's get out */
        $('span#loginmsg').html(data.msg);
        if (data.status === 'ok') {
            $('span#loginmsg').addClass('alert-success');
            auth.userAuthenticated(data.msg.user);
            $('span#loginmsg').fadeIn();
        } else {
            $('span#loginmsg').addClass('alert-error');
            $('span#loginmsg').fadeIn();
        }

        window.setTimeout(function(){
            $('span#loginmsg').fadeOut();
        },5000);
    }

    $('#frmLogin').ajaxForm({
        dataType: 'json',

        beforeSubmit: function () { handleBeforeSubmit($('#frmLogin')); },
        success: function (data) { handleSuccess($('#frmLogin'), data); }
    });


    $('#remember_password').ajaxForm({
        dataType: 'json',
        beforeSubmit: function () { handleBeforeSubmit($('#frmLogin')); },
        success: function (data) { handleSuccess($('#frmLogin'), data); }
    });

    $('span#loginmsg').hide();
    $('.passwordReminder').hide();
    $('#signupoverlay').hide();
    $('#tos').hide();

    auth.callback_login = function(action){
        //alert('callback:' + action);
        if( $('#iframevotacao') ){
            var ifr = $('#iframevotacao')[0];
            try{
                if(ifr.contentWindow && ifr.contentWindow.trata_botao_adicionar_ideia){
                    var pode = action == 'login';
                    ifr.contentWindow.trata_botao_adicionar_ideia(pode);
                }
            }catch(erro){ }
        }
    };

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

});

$(document).ready(function(){
   $.getJSON("http://search.twitter.com/search.json?rpp=100&callback=?&q=%23transitors",function(data){
        console.log(data);
        for(var i=0; i < 20 && i < data.results.length; i++){
            option = {
                title: '@'+data.results[i].from_user_name,
                content: data.results[i].text,
                trigger: 'hover',
                placement: 'right',
            };
            var number = 1 + Math.floor(Math.random() * 8);
            $('.tweets ul').prepend("<li class='pessoa"+number+"' id='"+i+"'> </li>");
            $('.tweets li').popover(option);
        }
   });
});
