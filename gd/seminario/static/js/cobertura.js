$(window).load(function() {
    $('#cancel').click(function(){
        $('#modallink').modal('hide')
    });

    $( "#link" ).change(function() {
        $.get('/seminario/getitle/',{'site':$(this).val()})
        .success( function(d){
            $('#nomedosite').val(d.title);
        });
        // alert( "Handler for .change() called." + $(this).val() );
    });

    $('a.link-col').click(function(){
        $.post('/seminario/av',{'i':$(this).attr('data-id')});
    });

    $("#novolink").ajaxForm({
        beforeSubmit: function () {
            $('#msg').fadeOut();
            $('#msgerror').fadeOut();
        },

        success: function (pData) {
            console.log(pData);
            // var pData = $.parseJSON(data);
            if (pData.status !== 0) {
                $('#msgerror')
                    .html(pData.msg)
                    .fadeIn('fast');
            } else {
                $('#msg')
                    .html(pData.msg)
                    .fadeIn('fast');
                $('#novolink').resetForm();
                $('#modallink').modal('hide')
                window.setTimeout(function(){
                    $('#msg').fadeOut('slow');
                },5000);
            }
            return false;
        }
    });


    $('#enviar').click(function(){

        console.log("Enviando link");

        $("#novolink").submit();

    });
});
