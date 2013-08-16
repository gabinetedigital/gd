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

    $('.event').toggle(function() {
        $(this).find('li.meta').slideDown('slow');
    },function(){
        $(this).find('li.meta').slideUp();
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

});
