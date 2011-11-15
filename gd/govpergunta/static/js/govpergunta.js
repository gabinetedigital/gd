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
            top: '10%',
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
            $('#themed ul.internal').data('tabs').click(0);
            this.update(0);
        },

        update: function (idx) {
            if (this.current === '')
                return null;

            var $el = $('a', $('ul.internal li').get(idx));
            var name = $el.attr('target');
            var $target =
                    $('div.' + name + ' .cont', $('.ptpanes')).html('');
            var url =
                    BASE_URL + 'pages/govpergunta/' +
                    themeapi.current + '/' + name + '.json';

            /* Saving the context */
            var self = this;

            /* The user asked to go to the contribute form */
            if (name === 'contribua') {
                navapi.click(3);
                $('a.theme').each(function () {
                    $(this).data('overlay').close();
                    $('#theme_' + self.current).attr('checked', 'checked');
                    $('.contribute label').removeClass('selected');
                    $('#theme_' + self.current)
                        .parent()
                        .find('label')
                        .addClass('selected');
                });
                return null;
            }

            $.getJSON(url, function (data) {
                /* Yes, if none is retrieved, we'll clean the
                 * element content. */
                var ct = (data !== null) ? data.content : '';
                $target.html(ct);
            });
            return $el;
        },

        goToContribForm: function () {
        }
    };

    /* -- Contribute page -- */

    $('.contribute label').click(function () {
        $('.contribute label').removeClass('selected');
        $(this).addClass('selected');
    });


    $('.contribute form').ajaxForm({
        beforeSubmit: function () {
            var form = $('.contribute form');
            form.find('input,textarea').removeClass('fielderror');
            form.find('.error').fadeOut();
            form.find('.errmsg').html('').hide();

            /* Saving the success callback to be called when the user
             * is properly logged */
            var options = this;
            if (!auth.isAuthenticated()) {
                auth.showLoginForm({
                    success: function () {
                        form.ajaxSubmit(options.success);
                    }
                });
                return false;
            }
            return true;
        },

        success: function (rdata) {
            var data = $.parseJSON(rdata);

            /* It's everything ok, let's get out */
            if (data.status === 'ok') {
                $('#form fieldset').fadeOut();
                $('div.success').fadeIn();
                return;
            }

            /* Here we know that something is wrong */
            var form = $('.contribute form');
            var code = data.code;
            var errors = data.msg;

            /* Just updating this object with received data */
            if (data.msg && data.msg.data)
                errors = data.msg.data;

            /* The first step now is to set the new csrf
             * token to our form. If we don't do it, we
             * can't try to register again. */
            if (data.msg.csrf !== undefined)
                form.find('[name=csrf]').val(data.msg.csrf);

            /* The user made a mistake when filling the form */
            if (code === 'ValidationError') {
                for (var f in errors) {
                    var msg = errors[f][0];
                    /* O lixo do wtforms não me deixou traduzir as strings
                     * que ele gera dinâmicamente. Logo, fiz marreta. */
                    if (f === 'theme')
                        msg = 'Escolha uma das opções acima';
                    form
                        .find('[name=' + f  + ']')
                        .addClass('fielderror');
                    form
                        .find('.'+ f + '-error')
                        .html(msg)
                        .show();
                    form.find('div.error')
                        .html('Falta alguma informação para completar a sua proposta')
                        .fadeIn('fast');
                }
            } else {
                form
                    .find('div.error')
                    .html(errors)
                    .fadeIn('fast');
            }
            return null;
        }
    });

    return new ThemeApi();
})();

function show_form_again() {
    $("#form .title").attr("value", "");
    $("#form textarea").val("");
    $('.contribute label').removeClass('selected');
    $("#form input[type=radio]").attr("checked",false);
    $('div.success').fadeOut(function () {
        $('#form fieldset').fadeIn();
    });
}