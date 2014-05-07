/* Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
 *
 *   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

function showAggregated(parentId) {
    $('#aggregated-' + parentId).slideToggle();
}


$('.enviarDesabilitado').click(function(){
    showNeedLogin($(this));
    return false;
});

var showNeedLogin = function(obj, msg){
        // var botaoentrar = $('#menu .entrar a');
        // console.log( obj );
        var cont = "O prazo para envio de perguntas foi encerrado no dia 7 de maio. <br>Mas você ainda pode votar até o dia 10 nas questões já enviadas.";
        if (msg != "" && msg != null) {
            cont = msg;
        }
        var options = {
            'content'      : cont,
            'title'     : "Envio encerrado",
            'animation' : true,
            'placement' : "left",
            'trigger'   : "manual"
        }
        obj.popover(options);
        obj.popover('show');

        window.setTimeout(function(){
            obj.popover('hide');
        },10000);
    };

function vote(qid, obj) {
    if (!auth.isAuthenticated()) {
        showNeedLogin($(obj));
        return false;
    }

    $.get(url_for('govresponde.vote.<qid>', { qid: qid }), function (data) {
        $('#question-' + qid + ' button').replaceWith(
            $('<div>')
                .addClass('success')
                .addClass('msg')
                .show()
                .html('Obrigado por votar. Seu voto foi contabilizado'));
        $('#question-' + qid + ' .score')
            .fadeOut(function () {
                $(this)
                    .html(data)
                    .fadeIn();
            });
    });

}

$('#mensagemfim').overlay({
    // some mask tweaks suitable for modal dialogs
    mask: {
        color: '#000',
        loadSpeed: 200,
        opacity: 0.6
    },
    load:  true,
    closeOnClick: false,
    closeOnEsc: false
});
