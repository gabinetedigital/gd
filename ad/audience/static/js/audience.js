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

/** Toggles the buzz filter status to on/off */
$(function() {
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

    new Buzz("localhost", {
        new_buzz: function (msg) {
            if (filterState) {
                var $el = $(tmpl("buzzTemplate", msg));
                $('#buzz').prepend($el);
            }
        }
    });
});
