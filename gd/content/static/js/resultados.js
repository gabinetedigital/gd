$(function(){
    $('.aggrlink').click(function() {
        $('.agregadas').slideToggle("slow");
        $('.thumbnails').masonry('reload');
    });

    $('.buttons .span3').click(function() {
        $('#board1' ).hide();
        $('#board2' ).hide();
        $('#board3' ).hide();
        $('#board4' ).hide();
        $('#' + $(this).attr('data-id') ).slideToggle("slow");
    });

    $('.dados').show();
    $('#board1' ).hide();
    $('#board2' ).hide();
    $('#board3' ).hide();
    $('#board4' ).hide();

    $('.detalhes').hide();

    $('.botaomais').click(function(){
        // alert( $(this).attr('data-id') );
        $('.detalhes').hide();
        var url = "/govpergunta/resultados-detalhe/" + $(this).attr('data-id')  + "/";
        $.ajax(url,{
            success: function(data, textStatus, jqXHR){
                // alert('Veio legal!');
                $('.detalhes').html(data);
                $('.detalhes').slideToggle("slow");
            }
        });
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
