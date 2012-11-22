$(function(){
    $('.aggrlink').click(function() {
        $('.agregadas').slideToggle("slow");
        $('.thumbnails').masonry('reload');
    });

    $('.buttons .span3').click(function() {
        $('.mais').hide();
        $('.agregadas').hide();
        $('.comments').hide();
        $('#board1' ).hide();
        $('#board2' ).hide();
        $('#board3' ).hide();
        $('#board4' ).hide();
        $('.lista').hide();
        if ($(this).attr('data-id') == "board1") {
            $('.lista').slideToggle();

        }
        $('#' + $(this).attr('data-id') ).slideToggle("slow");
        $('.thumbnails').masonry('reload');
        if ($(this).attr('data-id') == "board1") {
            $('html, body').stop().animate({
                'scrollTop': $('.lista').offset().top
            }, 500, 'swing');
        }
    });

    $('.dados').show();
    $('#board1' ).hide();
    $('#board2' ).hide();
    $('#board3' ).hide();
    $('#board4' ).hide();
    $('.lista').hide();

    $('.detalhes').hide();


    chamadetalhes = function(postid){
        $('.detalhes').hide();
        var url = "/govpergunta/resultados-detalhe/" + postid  + "/";
        $.ajax(url,{
            success: function(data, textStatus, jqXHR){
                // alert('Veio legal!');
                chamadetalhes.LAST_CALLED_ID = postid;
                $('.detalhes').html(data);
                $('.detalhes').slideToggle("slow");
                $('html, body').stop().animate({
                    'scrollTop': $('.mais').offset().top
                }, 500, 'swing');
            }
        });
    };
1
    chamadetalhes.LAST_CALLED_ID = 0;

    auth.callback_login = function (action) {
        //alert(action + '=' + chamadetalhes.LAST_CALLED_ID);
        if(chamadetalhes.LAST_CALLED_ID != 0){
            chamadetalhes(chamadetalhes.LAST_CALLED_ID);
        }
    };

    $('.botaomais').click(function(){
        // alert( $(this).attr('data-id') );
        chamadetalhes( $(this).attr('data-id') );
    });

    $('#slideshow .controls').tabs('ul.carousel > li', {
        effect: 'fade',
        rotate: true
    }).slideshow({
        clickable: false
    });

    if ($('#slideshow .controls').length > 0) {
        window.setInterval(function () {
            $("#slideshow .controls").data("tabs").next();
        }, 7000);
    }

});
