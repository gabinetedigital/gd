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

    $('.commentform').ajaxForm({
        dataType: 'json',
        beforeSubmit: function (fields, myform, xhr) {

            $val = $(myform).find("#content").val();
            if( $val.length < 3 ){
                alert('É necessário informar mais de 3 caracteres no comentário!');
                return false;
            }else{
                $('.alert').remove();
            }
        },
        success: function (data, status, xhr, myform) {
            $(myform).parent().prepend("<div class='alert alert-success'>"+data.msg+"</div>");
            $(myform).find("#content").val("");
        }
    });

   $('.issoEImportante a.votar').not('.voted').unbind().on("click",function(){
        var url = $(this).attr('data-url');
        var _clicado_ = $(this)
        _clicado_.attr('disabled','disabled');
        if(url){
            $.get(url, function(data){
                var pData = $.parseJSON(data);
                _clicado_.parent().parent().find(".counter").html(pData.score);
                _clicado_.removeAttr('href');
                _clicado_.removeAttr('data-url');
                _clicado_.find('div.curtir').addClass("voted");
            });
        }

       return false;
    });


   $('#sigaObraForm').ajaxForm({
        success:function(data){
            var pData = $.parseJSON(data);
            if (pData.status != 'ok'){
                alert(pData.msg);
            }else{
                if(pData.msg){
                    alert(pData.msg);
                }else{
                    alert('Obrigado! Agora você receberá informações sobre esta obra quando houver atualização.');
                }
            }
            $('.ajaxform input[type=submit]').removeAttr('disabled');
        },
        beforeSubmit: function (arr, form, options) {
            form.find('input[type=submit]').attr('disabled','disabled');
        }
    });

    $('#sigaObraBox .deseguir').click(function(){
        var url = $(this).attr('data-url');
        $('#sigaObraForm').ajaxSubmit({
            url: url,
            success:function(data){
                var pData = $.parseJSON(data);
                if (pData.status != 'ok'){
                    alert(pData.msg);
                }else{
                    if(pData.msg){
                        alert(pData.msg);
                    }else{
                        alert('Agora você não receberá mais informações sobre esta obra.');
                    }
                }
                $('.ajaxform input[type=submit]').removeAttr('disabled');
            },
            beforeSubmit: function (arr, form, options) {
                form.find('input[type=submit]').attr('disabled','disabled');
            }
        });
    });


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
        if( !$('#slfiltro').val() ){
            //Isto é para não enviar parametros vazios na URL
            $("input[name=filtro]").removeAttr('name');
            $("input[name=valor]").removeAttr('name');
        }
        $('#frmfilterbox').submit();
    });

    $('#slsecretaria, #slmunicipio, #slregiao').change(function(ev){

        var filtro = $('#slfiltro').val();
        $("input[name=filtro]").val( filtro );

        var vlr = $(this).val();
        $("input[name=valor]").val( vlr );

        if( !$('#slordem').val() ){
            //Isto é para não enviar parametros vazios na URL
            $("input[name=ordem]").removeAttr('name');
        }
        if( !$('#slfiltro').val() ){
            //Isto é para não enviar parametros vazios na URL
            $("input[name=filtro]").removeAttr('name');
            $("input[name=valor]").removeAttr('name');
        }
        $('#frmfilterbox').submit();
    });

    $('#slfiltro').change(function(ev){
        $('#filtros div.top').hide();
        var filtro = $(this).val();
        $('#div'+filtro).show();

        //Se selecionar "TODAS" limpa os filtros e recarrega
        if( !$(this).val() ){
            //Isto é para não enviar parametros vazios na URL
            $("input[name=filtro]").removeAttr('name');
            $("input[name=valor]").removeAttr('name');
            $('#frmfilterbox').submit();
        }

    });

    $('div.styled-select span i').click(function(){
        var sel = $(this).parent().parent().find("select");

        //TODO: Achar uma forma de abrir a caixa de seleção do select.
        // var size = sel.find('option').size();
        // if (size != sel.prop('size')) {
        //     sel.prop('size', size);
        // } else {
        //     sel.prop('size', 1);
        // }

    });

    $('.lb-image-down').click(function(){
        var src = $(this).parents("div#lightbox").find('.lb-container').find('.lb-image').attr('src');
        window.open(src);
    })


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
