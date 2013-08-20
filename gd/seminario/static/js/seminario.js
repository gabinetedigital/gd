$(window).load(function() {
    // $('#ascensor').ascensor({
    //     overflow: 'hidden'
    // });

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

    $('.event').click(function() {
        $('li.place span').text('+');
        $('li.meta').slideUp();
        if( $(this).find('li.meta').is (':hidden')) {
            $(this).find('li.meta').slideDown('slow');
            $(this).find('li.place span').text('-');
        }
    });

    $("#frminscricao").ajaxForm({
        beforeSubmit: function () {
            $('#msg').fadeOut();
            $('#msgerror').fadeOut();
        },

        success: function (pData) {
            // console.log(pData);
            // var pData = $.parseJSON(data);
            if (pData.status !== 0) {
                $('#msgerror')
                    .html(pData.msg)
                    .fadeIn('fast');
            } else {
                $('#msg')
                    .html(pData.msg)
                    .fadeIn('fast');
                $('#frminscricao').resetForm();
                window.setTimeout(function(){
                    $('#msg').fadeOut('slow');
                },5000);
            }
            return false;
        }
    });

    $('#colaborativa').click (function (){
        if ($(this).is (':checked')) {
            $('.modo_cobertura').fadeIn()
        }else{
            $('.modo_cobertura').fadeOut()
        }
    });

    $(".thumbnail").click(function(e){
        var bio = $(this).find(".minibio");
        $.fancybox.open(bio, {
            'maxWidth': 600
        });
        console.log("blah!");
    });

});
