var overlay_openned = false;

chamaLogin = function(){
	var mylink = document.getElementById("botao-login");
	mylink.click();
}

showParticipar = function(slug){
	//Caregga a página com o slug abaixo para a div
	//$('#ptcp').empty();
	$.getJSON('/pages/instrucoes-participar.json', function(pagina){

		//Abre este conteudo carregado + uma caixa de inserção de texto para 
		//a participação do usuário.
		//alert(pagina.content);

		if(!overlay_openned){
			$('#ptcp').prepend(pagina.content);
			$('#ptcp').prepend("<h1>" + pagina.title + "</h1>");
			//$('#ptcp').append("<br/>");
			overlay_openned = true;
		}		

	});

}

$('#botaoparticipar').overlay({
	// some mask tweaks suitable for modal dialogs
	mask: {
		color: '#c5c5c5',
		loadSpeed: 200,
		opacity: 0.9
	},
	closeOnClick: false,
	closeOnEsc: false
});
