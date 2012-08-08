var overlay_openned = false;

chamaLogin = function(){
	var mylink = document.getElementById("botao-login");
	mylink.click();
}

showParticipar = function(){

	if (show_comment_form){

		if(!overlay_openned){
			$.getJSON('/pages/instrucoes-participar.json', function(pagina){

				//Abre este conteudo carregado + uma caixa de inserção de texto para
				//a participação do usuário.
				//alert(pagina.content);
				$('#ptcp').prepend( pagina.content );
				$('#ptcp').prepend("<h1>" + pagina.title + "</h1>");
				//$('#ptcp').append("");
				overlay_openned = true;

			});
		}

		$('#div-nomeacao').hide();
		$('#div-alteracao').hide();
		$('#botoes-escolha').show();

		$('#blog_comment_form #categoria_sugestao').find('option[value=""]').attr('selected',true);
        $('#blog_comment_form #content1').val('');
        $('#blog_comment_form #content2').val('');


	}else{
		chamaLogin();
		return false;
	}

}

showMore = function(slug){

	$.getJSON('/pages/'+slug+'.json', function(pagina){

		//Abre o conteudo carregado em na caixa "overlay"
		//$('#showmore').empty();
		$('#showmore #content').html(pagina.content);
		$('#showmore #content').prepend("<h1>" + pagina.title + "</h1>");
		//$('#showmore').append("<button type='button' class='close'>&nbsp;</button>");

	});

}

clickNomeacao = function(){
	//$('#div-alteracao').hide();
	$('#botoes-escolha').fadeOut();
	$('#div-nomeacao').fadeIn();

};

clickAlteracao = function(){
	//$('#div-nomeacao').hide();
	$('#botoes-escolha').fadeOut();
	$('#div-alteracao').fadeIn();
};


$('#botaoparticipar').overlay({
	// some mask tweaks suitable for modal dialogs
	mask: {
		color: '#000',
		loadSpeed: 200,
		opacity: 0.9
	},
	closeOnClick: false,
	closeOnEsc: false
});

$('.showmore').overlay({
	// some mask tweaks suitable for modal dialogs
	mask: {
		color: '#000',
		loadSpeed: 200,
		opacity: 0.9
	},
	closeOnClick: false,
	closeOnEsc: false
});

/* ------------------------------------------ PARA OS ENVIOS DOS COMENTARIOS ----------------- */

$('#blog_comment_form').ajaxForm({
    beforeSubmit: function () {

        var form = $('#blog_comment_form');

        if( $('#div-nomeacao').is(':visible') ){

        	var field = form.find('select');
	        if ($.trim(field.val()) === '') {
	            field.addClass('fielderror');
	            return false;
	        } else {
	            field.removeClass('fielderror');
	        }

        	var field = form.find('#content1');
	        if ($.trim(field.val()) === '') {
	            field.addClass('fielderror');
	            return false;
	        } else {
	            field.removeClass('fielderror');
	        }

        }else{
        	if( $('#div-alteracao').is(':visible') ){

	        	var field = form.find('#content2');

		        if ($.trim(field.val()) === '') {
		            field.addClass('fielderror');
		            return false;
		        } else {
		            field.removeClass('fielderror');
		        }


        	}
        }

        /* Saving the success callback to be called when the user is
         * properly logged */
        var options = this;
        if (!auth.isAuthenticated()) {
            auth.showLoginForm({
                success: function () {
                    form.ajaxSubmit(options.success);
                    return true;
                }
            });
            return false;
        }
        return true;
    },

    success: function (data) {
        var pData = $.parseJSON(data);

        /* It's everything ok, let's get out */
        if (pData.status === 'ok') {
            $('div.error').fadeOut();
            $('div.success').fadeIn().html(pData.msg);

			$('#div-nomeacao').hide();
			$('#div-alteracao').hide();
			$('#botoes-escolha').show();

			$('#blog_comment_form #categoria_sugestao').find('option[value=""]').attr('selected',true);
	        $('#blog_comment_form #content1').val('');
	        $('#blog_comment_form #content2').val('');

        } else {
            $('div.success').fadeOut();
            $('div.error').fadeIn().html(pData.msg);
        }
    }
});
