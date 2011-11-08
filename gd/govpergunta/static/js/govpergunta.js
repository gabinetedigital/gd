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
   $("#question-writer").ghost_typer({
     text:'Como podemos melhorar o atendimento na saúde pública?',
     speed: 80
   });

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
            "div.ptpanes > div", {
                effect: 'fade', onBeforeClick: function (evt, idx) {
                    themeapi.update(idx);
                }
            });

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
            $('#themed')
                .attr('class', '')
                .addClass('overlay')
                .addClass(name);

            $('#themed h1').html(label);
            $('#themed ul.allThemes li.' + name).hide();
            $('#themed ul.allThemes li[class~=' +
              this.current + ']').fadeIn();
            this.current = name;
            console.debug('clicking');
            $('#themed ul.internal').data('tabs').click(0);
            this.update(0);
        },

        update: function (idx) {
            if (this.current === '')
                return null;

            var $el = $('a', $('ul.internal li').get(idx));
            var $target = $('div.' + $el.attr('target') + ' .cont',
                            $('.ptpanes')).html('');
            var url =
                    BASE_URL + 'pages/govpergunta/' +
                    themeapi.current + '/' +
                    $el.attr('target') + '.json';
            $.getJSON(url, function (data) {
                /* Yes, if none is retrieved, we'll clean the
                 * element content. */
                var ct = (data !== null) ? data.content : '';
                $target.html(ct);
            });
            return $el;
        }
    };

    return new ThemeApi();
})();
