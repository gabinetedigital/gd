/* -*- Mode: js2; c-basic-offset:4; -*-
 *
 * Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
 *
 *   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
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

$(function() {

    // Initializing "how it works" stuff
    $('a[rel]').overlay({
        oneInstance: false,
        speed: 'fast',
        fixed: false,
        mask: {
            color: '#111',
            opacity: 0.7
        },

        onLoad: function () {
            if ($(this.getOverlay()).data('firstRun') === undefined) {
                audience_show_how_it_works();
                $(this.getOverlay()).data('firstRun', 1);
            }
        }
    });

});

function audience_how_it_works_spinning_gears_setup() {
  var big_gear = $("#how-it-works-big-gear");
  var small_gear = $("#how-it-works-small-gear");
  var how_it_works = $("#how-it-works");

  big_gear.data("angle",0);
  small_gear.data("angle",0);

  var timer = new Timer();
  timer.then(function(timer,accel) {
    var big_current_angle = big_gear.data("angle");
    var small_current_angle = small_gear.data("angle");

    var big_angle = (big_current_angle + (Math.log(accel+2))) % 360;
    var small_angle = (small_current_angle - (Math.log(accel+2))) % 360;

    big_gear.data("angle",big_angle);
    small_gear.data("angle",small_angle);

    big_gear.rotate(big_angle);
    small_gear.rotate(small_angle);

    if (accel == 0) timer.stop();
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
      });
    });
}

function audience_show_how_it_works() {
  var couple = $(".step-1-couple");
  var mail = $(".step-1-mail");
  var trail = $(".step-1-mail-trail");

  var big_gear = $(".step-2-big-gear");
  var small_gear = $(".step-2-small-gear");

  big_gear.data("angle",0);
  small_gear.data("angle",0);

  var step_2 = $(".step-2");

  var gentleman = $(".mustache-gentleman");
  var step_3_text = $(".step-3 p");
  var dialog = $(".mustache-gentleman-dialog");


  var spinning_gears = null;
  function spin_gears() {
      spinning_gears = setInterval(function() {
      var big_angle = (big_gear.data("angle")+1) % 360;
      var small_angle = (small_gear.data("angle")-1) % 360;

      big_gear.data("angle",big_angle);
      small_gear.data("angle",small_angle);

      big_gear.rotate(big_angle);
      small_gear.rotate(small_angle);
      }, 13);
  }

  // the animation...
  var timer = new Timer();

  timer.then(function(timer, step) {   /* step 1 */
    var opacity = step * 4 / 100.0;
    if (opacity > 1) opacity = 1;
    couple.css("opacity", opacity);
    if (opacity == 1) timer.next();

  }).then(function(timer,step) {
    var left = parseInt(mail.css("left"))+1;
    mail.css("left", left+"px");

    var opacity = parseFloat(mail.css("opacity")) + 0.05;
    if (opacity > 1) opacity = 1;

    mail.css("opacity", opacity);
    trail.css("opacity", opacity/2);

    if (left == 0) timer.next();
  }).then(function(timer) { /* step 2 */
    if (!spinning_gears) spin_gears();

    var opacity = parseFloat(step_2.css("opacity")) + 0.05;
    if (opacity > 1) opacity = 1;
    step_2.css("opacity", opacity);

    if (opacity == 1) timer.next();
  }).then(function(timer) { /* step 3 */
    var opacity = parseFloat(gentleman.css("opacity")) + 0.05;
    if (opacity > 1) opacity = 1;
    gentleman.css("opacity", opacity);
    step_3_text.css("opacity", opacity);
    dialog.css("opacity",opacity);
    if (opacity == 1) timer.next();
  }).then(function(timer) {
    if (!dialog.is(":visible")) {
      dialog.animate({
        width: 'toggle'
      }, 1000, 'swing');
    }
    timer.next();
  });

  timer.run();
}

function show_how_to() {
    $("#saiba-mais-link").hide();
    $("#saiba-mais-text").show();
}
