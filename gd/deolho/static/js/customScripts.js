$( "#linkSaibaMais" ).click(function() {
    $( "#additionalInfo" ).toggle( "slide", 'slow' );
});

$( "#fiscalizeObra" ).click(function() {
    $( "#fiscalizeObraBox" ).toggle('normal');
});

$( "#sigaObra" ).click(function() {
    $( "#sigaObraBox" ).toggle('normal');
});


$( "#compartilhaObra" ).click(function() {
    $( "#compartilhaObraBox" ).toggle('normal');
});




//================================================================================================================================================
$(document).ready(function() {
    $(".toggle-trigger").click(function() {
        $(this).parent().nextAll('.toggle-wrap').first().toggle('normal');
    });
});



function GetURLParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
}
$(function() {

    //Verifica se está ordenado e ajusta o select
    var ordenado = GetURLParameter("o");
    if(ordenado){
        $('#slordem').val(ordenado);
    }

    $('#slordem').change(function(ev){
        var ordem = $(this).val();
        // window.location.href = window.location.href.replace( /[\?#].*|$/, "?single" );
        console.log(ev);
        console.log("ORDEM", ordem);
        var newurl = "";
        if(ordem){
            newurl = window.location.href.replace( /[\?#].*|$/, "?o="+ordem );
        }else{
            newurl = window.location.href.replace( /[\?#].*|$/, "" );
        }
        console.log("URL", newurl);
        window.location.href = newurl;
    });

    $('#slfiltro').change(function(ev){
        console.log("CHANGED FILTRO!");
        $('#filtros div').hide();
        console.log("HIDE FILTRO!");
        var filtro = $(this).val();
        console.log("FILTRO:",filtro);
        $('#div'+filtro).show();
    });

});
