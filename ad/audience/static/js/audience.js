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
        if (filterState) {
            $(this).addClass('off');
        } else {
            $(this).removeClass('off');
        }
        $.getJSON(url, function (data) {
            var $root = $('#buzz');
            $root.html('');
            $(data).each(function (index, item) {
                $(tmpl('buzzTemplate', item)).appendTo($root);
            });
        });
    });


    /** Shows a tooltip of an element with manual control of show/hide
     *  operations */
    function showTooltip(elementOrSelector) {
        if (typeof elementOrSelector === 'string') {
            $element = $(elementOrSelector);
        } else {
            $element = elementOrSelector;
        }

        var $tooltip = $element.tooltip({
            effect: "fade",
            delay: 4200,
            opacity: 0.7,
            events: {
                input: 'customOpenEvent,customOpenEvent'
            }
        });
        $element.trigger('customOpenEvent');
        return $tooltip;
    }


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
                    auth.showLoginForm({
                        success: function (userData) {
                            postNotice(message);
                        }
                    });
                    return;
                } else {
                    // Feedback the user. something wrong happened.
                    showTooltip(
                        $("#internal_chat textarea")
                            .attr('title', parsedData.msg));
                }
            } else {
                // Everything' fine, let's just clear the message box
                // and thank the user
                var $textbox = $("#internal_chat textarea")
                    .val('')
                    .attr('title', parsedData.msg);
                showTooltip($textbox);

                window.setTimeout(function () {
                    $textbox.attr('title', '');
                }, 10000);
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

    $('a.filter').tooltip({ opacity: 0.7 });

    // Starts a new instance of the buzz stream

    function updateBuzz(msg, show) {
        if (show) {
            var $el = $(tmpl("buzzTemplate", msg));
            $('#buzz').prepend($el);
        }
    }

  function Timer(interval) {
    var self = this;
    self._fns = [];
    self._idx = 0;
    self._current = null;
    //self._step = 0;
    self._flag = null
    self._stepper = null;
    self._running = false;

    self.then = function(fn) {
      self._fns.push(fn);
      return self;
    }

    self.stepper = function(fn) {
      self._stepper = fn;
    }

    self.run = function() {
      self._running = true;
      self._idx = 0;
      self.exec();
    }

    self.exec = function() {

      self._current = setInterval(function() {
        self._fns[self._idx](self, self._stepper(), self._flag)
      }, interval);
    }

    self.next = function() {
      clearInterval(self._current);
      self._idx++;
      self.exec();
    }

    self.flag = function(arg) {
      self._flag = arg;
    }

    self.stepper = function(fn) {
      self._stepper = fn;
    }

    self.isRunning = function() {
      return self._running;
    }

    self.stop = function() {
      self._running = false;
      clearInterval(self._current);
    }
  }

  //how it works spinning gears
  (function() {

    var big_gear = $("#how-it-works-big-gear");
    var small_gear = $("#how-it-works-small-gear");
    var how_it_works = $("#how-it-works");
    var interval = 13;

    big_gear.data("angle",0);
    small_gear.data("angle",0);

    timer = new Timer(interval);
    timer.then(function(timer,accel) {
      //console.log(accel);
      var big_current_angle = big_gear.data("angle");
      var small_current_angle = small_gear.data("angle");

      var big_angle = (big_current_angle + (Math.log(accel+2))) % 360;
      var small_angle = (small_current_angle - (Math.log(accel+2))) % 360;

      big_gear.data("angle",big_angle);
      small_gear.data("angle",small_angle);

      big_gear.rotate(big_angle);
      small_gear.rotate(small_angle);

      if (accel == 0) timer.stop()
    });

    var accel = 0;
    var max_accel = 100;
    how_it_works.hover(
      function() {
        timer.stepper(function() {
          if (accel < max_accel) accel++;
          return accel;
        });
        if (!timer.isRunning()) timer.run();
      },
      function() {
        timer.stepper(function() {
          if (accel > 0) accel--;
          return accel;
        })
      });
  })();

    new Buzz(SIO_BASE, {
        new_buzz: function (msg) {
            updateBuzz(msg, filterState);
        },

        buzz_accepted: function (msg) {
            updateBuzz(msg, !filterState);
        }
    });
});
