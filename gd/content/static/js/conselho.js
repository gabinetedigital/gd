chamaLogin = function(){
	var mylink = document.getElementById("botao-login");
	mylink.click();
}

showParticipar = function(slug){
	//Caregga a página com o slug abaixo para a div
	$('#ptcp').empty();
	$.getJSON('/pages/instrucoes-participar.json', function(pagina){

		//Abre este conteudo carregado + uma caixa de inserção de texto para 
		//a participação do usuário.
		//alert(pagina.content);
		
		$('#ptcp').append("<h1>" + pagina.title + "</h1>");
		$('#ptcp').append(pagina.content);
		$('#ptcp').append("<br/><form><textarea id='participar-texto' rows='15' cols='75'></textarea><br/><br/><div class='right'><button type='button' class='awesome'>Enviar</button>&nbsp;<button type='button' class='awesome'>Fechar</button></div></form>");
		

	});

}

$('#botaoparticipar').overlay({
	// some mask tweaks suitable for modal dialogs
	mask: {
		color: '#ebecff',
		loadSpeed: 200,
		opacity: 0.9
	},
	closeOnClick: false
});