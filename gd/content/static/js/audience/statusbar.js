/* Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
 *
 *   Author: Thiago Silva <thiago@metareload.com>
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

/*
 * A simple "status bar" tool.
 *
 * Each status bar should be registered with a name.
 * ie:
 *    $(<target>).status_bar(name)
 *
 *  Status messages are delivered to specific status bar with:
 *
 *    var hide = $.status_message({target: name, message: msg})
 *
 *  The message is displayed for 10 seconds before slidingUp
 *  (interval may be passed as parameter to status_message)
 *
 *  If interval is 0, message is not hidden.
 *
 *  status_message returns a function that hides
 *  the message when called.
 *
 * Status messages are cumulative: many messages
 * can be sent to a bar which will be displayed
 * below each other.
 */

$(function() {
    var statusbars = {};
    $.fn.status_bar = function(name) {
        statusbars[name] = $(this);
        statusbars[name].hide();
    },

    $.status_message = function(spec) {
        var name = spec.tag; //the bar name
        var msg = spec.message;
        var interval = spec.interval || 10000;

        var bar = statusbars[name];
        var msg_node = $("<p>"+msg+"</p>").hide();

        bar.append(msg_node);
        msg_node.slideDown();

        if (!bar.is(":visible")) {
            bar.slideDown();
        }

        function dismiss() {
            msg_node.slideUp(300, function() {
                msg_node.detach();
                if (bar.children().length == 0) {
                    bar.slideUp();
                }
            });
        }

        if (interval > 0) {
            setTimeout(dismiss, interval);
        }
        return dismiss;
    }
});