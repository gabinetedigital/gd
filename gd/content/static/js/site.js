/* Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Thiago Silva <thiago@metareload.com>
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

$(function () {
    /* The code responsible for the interaction of the  "Participate"
     * button. Yes, that big red button in the middle of the screen :) */
    function toggle() {
        var $participe = $('#participe');
        var $slideshow = $('#slideshow');
        if ($participe.is(':visible')) {
            $participe.show().slideUp();
            $slideshow.hide().slideDown();
        } else {
            $slideshow.show().slideUp();
            $participe.hide().slideDown();
        }
    }
    $("#a-participe").click(toggle);
    $("#participe .close").click(toggle);

    /* -- Show/hide text on the mouse over event in "participate" buttons -- */
    $("#participe .govresponde")
        .data('text','Quer saber o que o Governador pensa? Pergunte para ele. ' +
              'A questão mais votada do mês é respondida em vídeo.');
    $("#participe .govpergunta")
        .data('text', 'O Governador pergunta e a sociedade responde com novas ' +
              'idéias.');
    $("#participe .agenda")
        .data('text', 'Quer fazer parte da agenda do Governador na sua cidade?' +
              ' Indique uma pauta na agenda colaborativa.');
    $("#participe .govescuta")
        .data('text','Audiências públicas digitais transmitidas via internet  ' +
              'onde você pode enviar sua contribuição.');

    $("#participe .govresponde, " +
      "#participe .govpergunta, " +
      "#participe .govescuta,   " +
      "#participe .agenda")
        .hover(function() {
            $(this).addClass('selected');
            $("#participe .desc").text($(this).data("text"));
        }, function() {
            $("#participe .desc").text('');
            $(this).removeClass('selected');
        });


    /* -- Supporting browsers that don't have the `placeholder' stuff -- */
    if (!('placeholder' in document.createElement('input'))) {
        $('input')
            .focus(function () {
                if ($(this).val() === $(this).attr('placeholder')) {
                    $(this).val('');
                }
            })
            .blur(function () {
                if ($(this).val() === '') {
                    $(this).val($(this).attr('placeholder'));
                }
            })
            .blur();
    }


    /* -- handling the "update your browser" message overlay -- */
    if (($.browser.msie && parseInt($.browser.version) < 8)) {
        $(".browser-banner").overlay({
            load:true,
            oneInstance: false,
            speed: 'fast',
            mask: {
                color: '#111',
                opacity: 0.7
            }
        });
    }

    /* -- sociable stuff -- */
    stLight.options({
        publisher:'12345'
    });

});
