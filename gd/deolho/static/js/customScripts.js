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
        var obraid = $(this).attr('data-id');
        $.get("/deolho/comments/"+obraid+"/", function (content) {
            $('#comentarios'+obraid).find(".com-content").html(content);
            $('#comentarios'+obraid).find("#content").val("");
        });
    });

    // console.log("AJAXFORM");
    // console.log( $('.commentform') );
    $('.commentform').ajaxForm({
        dataType: 'json',
        beforeSubmit: function (fields, myform, xhr) {
            // console.log(p1,p2,p3,p4);
            $('.alert').remove();
        },
        success: function (data, status, xhr, myform) {
            // console.log(status, myform);
            // console.log("data",data);
            $(myform).parent().append("<div class='alert alert-success'>"+data.msg+"</div>");
            $(myform).find("#content").val("");
        }
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
    if(valorf){
        valorf = decodeURIComponent(valorf.replace( /\+/, " " ));
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

    $('div.styled-select span i').click(function(){
        console.log("CLIDADO NA SETINHA");
        var sel = $(this).parent().parent().find("select");

        //TODO: Achar uma forma de abrir a caixa de seleção do select.
        // var size = sel.find('option').size();
        // if (size != sel.prop('size')) {
        //     sel.prop('size', size);
        // } else {
        //     sel.prop('size', 1);
        // }

    });

});
