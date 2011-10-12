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
    // Toggles the buzz filter status to on/off.
    //
    // Control var that holds the state of the filter button. Set it to
    // true to show moderated buzz and false for the public messages.
    var filterState = false;
    $('a.filter').click(function() {
        var url = CURRENT_URL + (
            filterState ? '/moderated_buzz' : '/public_buzz');
        filterState = !filterState;
        $.getJSON(url, function (data) {
            var $root = $('#buzz');
            $root.html('');
            $(data).each(function (index, item) {
                $(tmpl('buzzTemplate', item)).appendTo($root);
            });
        });
    });


    /** Posts a new notice on the message buzz */
    function postNotice(message) {
        var params = { aid: $('#aid').val(), message: message };
        $.post(url_for('buzz.post'), params, function (data) {
            var parsedData = $.parseJSON(data);
            if (parsedData.status !== 'ok') {
                // For any reason, the user got loged out, so, as it's
                // an async call, we have to request login credentials
                // again. It's not actually usual to happen but better
                // being safe than sorry.
                if (parsedData.code === 'NobodyHome') {
                    auth.shpowLoginForm({
                        success: function (userData) {
                            postNotice(message);
                        }
                    });
                    return;
                }

                // Feedback the user. something wrong happened.
            } else {
                // Everything' fine, let's just clear the message box
                // and thank the user
                var $textbox = $("#internal_chat textarea");
                $textbox.val('');
            }
        });
    }


    $('#internal_chat').submit(function () {
        var $form = $(this);
        var $field = $('textarea', $form);
        var aid = $('#aid').val();
        var data = $.trim($field.val());

        // None received in the form. We cannot process this
        // request. Just feedback the user.
        if (data === '') {
            $field.addClass('error');
            return false;
        }

        // Just making sure that the user will not be confused by any
        // old error report.
        $field.removeClass('error');

        // Not authenticated users must access the login form
        if (!auth.isAuthenticated()) {
            auth.showLoginForm({
                success: function (userData) {
                    postNotice(data);
                }
            });
        } else {
            // Time to send the request to the server
            postNotice(data);
        }
        return false;
    });

    // Starts a new instance of the buzz stream

    function updateBuzz(msg, show) {
        if (show) {
            var $el = $(tmpl("buzzTemplate", msg));
            $('#buzz').prepend($el);
        }
    }

    new Buzz("localhost", {
        new_buzz: function (msg) {
            updateBuzz(msg, filterState);
        },

        buzz_accepted: function (msg) {
            updateBuzz(msg, !filterState);
        }
    });
});
