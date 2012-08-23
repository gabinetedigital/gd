$(function(){
    var sticky_navigation_offset_top = $('.subnav').offset().top;
    var sticky_navigation = function(){
        var scroll_top = $(window).scrollTop();
        if (scroll_top > sticky_navigation_offset_top) {
            $('.subnav').addClass('subnav-fixed');
            $('.tools').show();
        } else {
            $('.subnav').removeClass('subnav-fixed');
            $('.tools').hide();
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

    option = {
        title: '@andrenano',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin lobortis ultricies nunc ac euismod. Class aptent taciti sociosqu ad volutpat.',
        trigger: 'hover',
        placement: 'right',
    };
    $('.tweets li').popover(option);

    $('.subnav').scrollspy()
});