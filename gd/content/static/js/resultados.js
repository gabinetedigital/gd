$(function(){
    $('.aggrlink').click(function() {
        $('.agregadas').slideToggle("slow");        
        $('.thumbnails').masonry('reload');
    });

    $('.buttons .span3').click(function() {
        $('.dados').slideToggle("slow");        
    });

});
