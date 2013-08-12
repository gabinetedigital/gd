$(window).load(function() {
    $('.section').css({'height':(($(window).height()))+'px'});

    $("#menu li a").tooltip();

    $('#menu a[href^="#"]').bind('click.smoothscroll',function (e) {
        e.preventDefault();
        var target = this.hash,
        $target = $(target);
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 500, 'swing', function () {
            window.location.hash = target;
        });
    });

    $('.event').toggle(function() {
        $(this).find('li.meta').slideDown('slow');
    },function(){
        $(this).find('li.meta').slideUp();
    });

});
