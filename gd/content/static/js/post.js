/* Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
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

    $("#time").click(function() {
        $("#timeline").overlay().load();
    });


    $("#timeline").overlay({
        mask: {
            color: '#111',
            loadSpeed: 200,
            opacity: 0.9
        },

        closeOnClick: true,
        load: true
    });

});

$('#blog_comment_form').ajaxForm({
    beforeSubmit: function () {
        var form = $('#blog_comment_form');
        var field = form.find('textarea');

        if ($.trim(field.val()) === '') {
            field.addClass('fielderror');
            return false;
        } else {
            field.removeClass('fielderror');
        }

        /* Saving the success callback to be called when the user is
         * properly logged */
        var options = this;
        if (!auth.isAuthenticated()) {
            auth.showLoginForm({
                success: function () {
                    form.ajaxSubmit(options.success);
                    return true;
                }
            });
            return false;
        }
        return true;
    },

    success: function (data) {
        var pData = $.parseJSON(data);

        /* It's everything ok, let's get out */
        if (pData.status === 'ok') {
            $('div.error').fadeOut();
            $('div.success').fadeIn().html(pData.msg);
            $('#blog_comment_form textarea').val('');
        } else {
            $('div.success').fadeOut();
            $('div.error').fadeIn().html(pData.msg);
        }
    }
});
