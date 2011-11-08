/* Copyright (C) 2011 Thiago Silva <thiago@metareload.com>
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


(function($) {
  $.fn.ghost_typer = function(spec) {
    var element = $(this);
    var text = spec.text;
    var speed = spec.speed === undefined ? 300 : spec.speed;
    var stop_on = spec.stop_on === undefined ? 4 : spec.stop_on;
    var start_on = spec.start_on === undefined ? 4 : spec.start_on;
    var on_finish = spec.on_finish || new Function;

    var caret_speed = 300;

    var caret = "|";

    function add_caret() {
      element.text(element.text()+caret);
    }

    function remove_caret() {
      var currentText = element.text();
      element.text(currentText.slice(0,currentText.length-1));
    }

    function blink_for(blinks,fn) {
      var i = 0;
      var caret_visible = true;
      var interval = setInterval(function() {
        if (i < blinks) {
          i++;
          if (caret_visible) {
            remove_caret();
          } else {
            add_caret();
          }
          caret_visible = !caret_visible;
        } else {
          clearInterval(interval);
          if(caret_visible) remove_caret();
          if (fn) fn();
        }
      }, caret_speed);
    }

    //

    function init() {
      element.text(caret);
      blink_for(start_on, start_writing)
    }

    function start_writing() {
      var i = 0;
      var interval = setInterval(function() {
        if (i < text.length) {
          remove_caret();
          element.text(element.text()+text[i++]);
          add_caret();
        } else {
          clearInterval(interval);
          blink_for(stop_on, on_finish);
        }
      },speed)
    }

    element.text("|")

    init();

    return $(this);
  }
})(jQuery);

