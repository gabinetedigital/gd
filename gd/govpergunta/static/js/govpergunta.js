/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
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

var navapi = null;

$(function () {
    var wizard = $('.wizard').data('isLoaded', false);

    $('#maintext, .tabs', wizard).click(function() {
        $('html,body').animate({ scrollTop: 320 }, 150);
    });

    $("ol.tabs", wizard).tabs(
        "div.panes > div", {
            effect: 'fade',
            lazy: true,
            onBeforeClick: function () {
                if (wizard.data('isLoaded')) {
                    $('html,body').animate({ scrollTop: 320 }, 150);
                }
            }
        });
    wizard.data('isLoaded', true);

    navapi = $("ol.tabs", wizard).data("tabs");

    // "next tab" button
    $(".next", wizard).click(function () {
        $('html,body').animate({ scrollTop: 320 }, 100);
	navapi.next();
    });

    // "previous tab" button
    $(".prev", wizard).click(function () {
        $('html,body').animate({ scrollTop: 320 }, 100);
	navapi.prev();
    });


    /* -- Setting up the per-theme description overlays --*/
    (function () {
        $('a.theme').overlay({
            top: '20%',
            speed: 'fast',
            fixed: false,
            oneInstance: false,
            mask: {
                color: '#111',
                opacity: 0.7
            }
        }).click(function () {
            themeapi.change(
                $(this).parent().attr('class'),
                $(this).attr('title')
            );
        });
 
        var $t1 = $('#themed');
        $('ul.internal', $t1).tabs(
            "div.ptpanes > div", { effect: 'fade' });

        var api = $('ul.internal', $t1).data('tabs');
        $('.next', $t1).click(function () { api.next(); });
        $('.prev', $t1).click(function () { api.prev(); });
    })();
});


var themeapi = (function () {

    function ThemeApi() {
        this.current = '';
    }

    ThemeApi.prototype = {
        change: function(name, label) {
            console.debug('pica no cu de satã');
            $('#themed')
                .attr('class', '')
                .addClass('overlay')
                .addClass(name);

            console.debug(this.current);
            $('#themed h1').html(label);
            $('#themed ul.allThemes li.' + name).hide();
            $('#themed ul.allThemes li[class~=' +
              this.current + ']').fadeIn();
            this.current = name;
        }
    };

    return new ThemeApi();
})();
