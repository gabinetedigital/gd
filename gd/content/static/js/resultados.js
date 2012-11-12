$(function(){
    $('.aggrlink').click(function() {
        $('.agregadas').slideToggle("slow");
        $('.thumbnails').masonry('reload');
    });

    $('.buttons .span3').click(function() {
        $('.dados').slideToggle("slow");
    });

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

});
