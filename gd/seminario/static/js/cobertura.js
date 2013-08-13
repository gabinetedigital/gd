$(window).load(function() {
    $('#cancel').click(function(){
        $('#modallink').modal('hide')
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
