/* Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
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

$(function() {
    $("ul.tabs").tabs("div.panes > form", function () {
        $('div.msg').hide();
        $('div.error').hide();
    });

    function handleBeforeSubmit(form) {
        form.find('*').removeClass('fielderror');
        return true;
    }

    function handleSuccess(form, data) {
        var errors = data.msg.data;
        var code = data.code;
        var csrfToken = data.msg.csrf;

        /* The first step now is to set the new csrf token to our
         * form. If we don't do it, we can't try to register
         * again. */
        form.find('[name=csrf]').val(csrfToken);

        /* It's everything ok, let's get out */
        if (data.status === 'ok') {
            $('div.msg').hide();
            $('div.error').fadeOut();
            $('div.success').fadeIn().html(data.msg.data);
        } else {
            $('div.msg').hide();
            $('div.success').fadeOut();
            $('div.error').fadeIn().html('Existem erros no formulário');
            for (var field in data.msg.data) {
                console.debug(field);
                $('[name=' + field + ']').addClass('fielderror');
            }
        }
    }

    $('#profile_form').ajaxForm({
        dataType: 'json',
        beforeSubmit: function () { handleBeforeSubmit($('#profile_form')); },
        success: function (data) { handleSuccess($('#profile_form'), data); }
    });

    $('#password_form').ajaxForm({
        dataType: 'json',
        beforeSubmit: function () { handleBeforeSubmit($('#password_form')); },
        success: function (data) { handleSuccess($('#password_form'), data); }
    });
});
