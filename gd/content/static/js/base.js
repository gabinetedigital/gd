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

    $('.clipping').hide();
    $('.publicacoes').hide();

    $('.clip').click(function(){
        $('.equipe').hide();
        $('.publicacoes').hide();
        $('.clipping').fadeIn();
    });

    $('.membros').click(function(){
        $('.clipping').hide();
        $('.publicacoes').hide();
        $('.equipe').fadeIn();
    });

    $('.pub').click(function(){
        $('.clipping').hide();
        $('.equipe').hide();
        $('.publicacoes').fadeIn();
    });


    var $container = $('.thumbnails');
    $container.imagesLoaded( function(){
        $container.masonry({
            itemSelector : '.thumbnails>li',
            columnWidth: function( containerWidth ) {
                console.log(containerWidth / 12);
                return containerWidth / 12;
            }
        });
    });

    // $(".scroll").scrollable({ circular: true }).autoscroll({ autoplay: true }).click(function() {
    //     $(this).data("scrollable").next();
    // });

    option = {
        title: '@andrenano',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin lobortis ultricies nunc ac euismod. Class aptent taciti sociosqu ad volutpat.',
        trigger: 'hover',
        placement: 'right',
    };
    $('.tweets li').popover(option);

    $('.subnav').scrollspy()

    $('.on').hide();
    $('.logado').hide();

    $('.entrar').click(function(){
        $('.off').hide();
        $('.on').fadeIn();
    });

    $('.form-inline').click(function(){
        $('.off').hide();
        $('.on').hide();
        $('.logado').fadeIn();
    });

});