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
    var filtrado = GetURLParameter("filtro");
    if(filtrado){
        $('#slfiltro').val(filtrado);
        $('#div'+filtrado).show();
        $("input[name=filtro]").val( filtrado );
    }
    var valorf = GetURLParameter("valor");
    //Metodo para retirar deixar os acentos corretor e retirar os '+'
    valorf = decodeURIComponent(valorf.replace( /\+/, " " ));
    if(valorf){
        $('#sl'+filtrado).val(valorf);
        $("input[name=valor]").val( valorf );
    }
    var ordenado = GetURLParameter("ordem");
    if(ordenado){
        $('#slordem').val(ordenado);
    }


    $('#slordem').change(function(ev){
        $('#frmfilterbox').submit();
    });

    $('#sltema, #slmunicipio, #slregiao').change(function(ev){

        // console.log("Changed...");
        var filtro = $('#slfiltro').val();
        $("input[name=filtro]").val( filtro );

        var vlr = $(this).val();
        console.log("VALOR DO FILTRO:",  vlr);
        $("input[name=valor]").val( vlr );

        $('#frmfilterbox').submit();
    });

    $('#slfiltro').change(function(ev){
        $('#filtros div').hide();
        var filtro = $(this).val();
        $('#div'+filtro).show();
    });


});
