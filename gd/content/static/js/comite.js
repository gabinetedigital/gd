$(function(){
    //auth.callback_login = function (action) {
	    //alert(action + '=' + chamadetalhes.LAST_CALLED_ID);
	    // if(chamadetalhes.LAST_CALLED_ID != 0){
	    //     chamadetalhes(chamadetalhes.LAST_CALLED_ID);
	    // }
    //};
    function ResetForm() {
        $(":input").not(":button, :submit, :reset, :hidden").each(function () {
            this.value = this.defaultValue;
        });
    };

    var enviarNoticia = function (){
    	if( $('#titulo').val() != "" && $('#noticia').val() ){

            $(".form-enviar-noticia").submit();

            //$('.msg').fadeOut();

			// $.ajax('/enviar-noticia/',{
   //              type: 'POST',
	  //           success: function(data, textStatus, jqXHR){
	  //               var pData = $.parseJSON(data);
   //                  alert(pData);
   //                  if (pData.status !== 'ok') {
   //                      $('#error')
   //                          .html(pData.msg)
   //                          .fadeIn('fast');
   //                  } else {
   //                      $('#success')
   //                          .html(pData.msg)
   //                          .fadeIn('fast');
   //                  }
   //                  return false;
	  //           }
	  //       });

    	}else{
    		alert('É necessário informar todos os campos.')
    	}

        return false;
    };

    $('.form-enviar-noticia button').click(function(e){
        e.preventDefault();
        if(!auth.isAuthenticated()){
            auth.showLoginForm({
                success: function () {
                    enviarNoticia();
                }
            });
        }else{
            enviarNoticia();
        }
    	return false;
    });

    $(".form-enviar-noticia").ajaxForm({
        beforeSubmit: function () {
            $('.msg').fadeOut();
        },

        success: function (data) {
            var pData = $.parseJSON(data);
            if (pData.status !== 'ok') {
                $('#error')
                    .html(pData.msg)
                    .fadeIn('fast');
            } else {
                $('#success')
                    .html(pData.msg)
                    .fadeIn('fast');
                ResetForm();
            }
            return false;
        }
    });

    $(".form-cadastrar").ajaxForm({
        beforeSubmit: function () {
            $('.msg').fadeOut();
        },

        success: function (data) {
            var pData = $.parseJSON(data);
            if (pData.status !== 'ok') {
                $('#error-cad')
                    .html(pData.msg)
                    .fadeIn('fast');
            } else {
                $('#success-cad')
                    .html(pData.msg)
                    .fadeIn('fast');
                ResetForm();
            }
            return false;
        }
    });


    $(".entenda").click(function(e){
        $('.entenda-content').show();
        $('.faca-content').hide();
        $('.envie-content').hide();
    });
    $(".faca").click(function(e){
        $('.entenda-content').hide();
        $('.faca-content').show();
        $('.envie-content').hide();
    });
    $(".envie").click(function(e){
        $('.entenda-content').hide();
        $('.faca-content').hide();
        $('.envie-content').show();
    });


});