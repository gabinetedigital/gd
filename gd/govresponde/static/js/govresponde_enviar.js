/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2011, 2012  Governo do Estado do Rio Grande do Sul
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

$(function () {
    $('form#send').ajaxForm({
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
                $('form#send ol,     ' +
                  'form#send .error, ' +
                  'form#send .errmsg ').fadeOut();
                $('div.success').fadeIn();
                return;
            }

            /* Here we know that something is wrong */
            var form = $('form#send');
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
                    // if (f === 'theme')
                    //     msg = 'Escolha uma das opções acima';
                    form
                        .find('[name=' + f  + ']')
                        .addClass('fielderror');
                    form
                        .find('.'+ f + '-error')
                        .html(msg)
                        .show();
                    form.find('div.error')
                        .html('Falta alguma informação para completar a sua contribuição')
                        .fadeIn('fast');
                }
            } else {
                form
                    .find('div.error')
                    .html(errors)
                    .fadeIn('fast');
            }
            return;
        }
    });
});

function showContribForm () {
    $("form#send .theme, form#send .title, form#send .question").val('');
    $('div.success').fadeOut(function () {
        $('form#send ol').fadeIn();
    });
}
