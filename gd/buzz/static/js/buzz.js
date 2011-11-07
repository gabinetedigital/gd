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

function Buzz(sockAddr, params) {
    var socket = new io.Socket(sockAddr);
    var args = $.extend({
        new_buzz: function (msg) {},
        buzz_accepted: function (msg) {},
        buzz_selected: function (msg) {},
        buzz_removed: function (msg) {},
        buzz_published: function (msg) {},
        buzz_unpublished: function (msg) {}
    }, params);

    /* Just starting the show */
    socket.connect();

    /* Should we do anything here? */
    socket.on('connect', function () { });

    /* This method receives the message from the socketio provider and
     * after that, calls the appropriated callback */
    socket.on('message', function (msg) {
        var parsed = JSON.parse(msg);
        var callback = args[parsed.message];
        if (callback !== undefined) {
            callback(parsed.data);
        }
    });

    /* Tries to reconnect if, for any reason, the user gets
     * disconnected. */
    socket.on('disconnect', function () {
        socket.connect();
    });
}
