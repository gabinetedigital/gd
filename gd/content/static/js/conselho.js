var overlay_openned = false;

chamaLogin = function(){
	var mylink = document.getElementById("botao-login");
	mylink.click();
}

showParticipar = function(){
	if(!overlay_openned){
		$.getJSON('/pages/instrucoes-participar.json', function(pagina){

			//Abre este conteudo carregado + uma caixa de inserção de texto para 
			//a participação do usuário.
			//alert(pagina.content);

			$('#ptcp').prepend(pagina.content);
			$('#ptcp').prepend("<h1>" + pagina.title + "</h1>");
			//$('#ptcp').append("");
			overlay_openned = true;

		});
	}

	$('#div-nomeacao').hide();
	$('#div-alteracao').hide();
	$('#botoes-escolha').show();


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

