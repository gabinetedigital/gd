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
    var moderatedBuzz = $("#buzz-moderated");
    var publicBuzz = $("#buzz-public");

    //max length of message a user can send
    var MAX_LENGTH = 300;

    // Increase textarea height on focus

    $('.droom #chat textarea').focusin(function(){
        $(".droom #chat textarea").switchClass( "tiny", "toon", 300 );
        return false;
    });

    $('.droom #chat textarea').focusout(function(){
        $(".droom #chat textarea").switchClass( "toon", "tiny", 300 );
        return false;
    });

    $('#bla').click(
        function() {
            $('#myModal').modal('toggle');
        }
    );

    $("a.filter").click(
        function() {
            $(this).toggleClass('off');
            moderatedBuzz.toggle();
            publicBuzz.toggle();
            if($('#buzz-public').is(':visible') ) {
            	new Buzz(BASE_URL, {
            		buzz_all: function (msg) {
                        $('#buzz-public').append($(tmpl("buzzTemplate", msg)));
                    }
                }, 'updatepage');
            } else {
            	$('#buzz-public').html('');            	
            }
        });

    // initializing status bar
    $("#message-statusbar").status_bar("message-statusbar");

    /** Posts a new notice on the message buzz */
    function postNotice(message) {
        var close_msg = $.status_message({
            tag: 'message-statusbar',
            message: 'Enviando mensagem...aguarde',
            interval: 0
        });

        var params = { aid: $('#aid').val(), message: message };
        $.ajax({
            url: url_for('buzz.post'),
            data: params,
            type:'post',
            error: function(_,text,err) {
                close_msg();
                $.status_message({
                    tag: 'message-statusbar',
                    message: 'Houve um erro ao enviar a mensagem'
                });
            },
            success: function (data) {
                close_msg();
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
                        $.status_message({
                            tag: 'message-statusbar',
                            message: parsedData.msg
                        });
                    }
                } else {
                    // delivery ok
                    $.status_message({
                        tag: 'message-statusbar',
                        message: parsedData.msg
                    });
                    clear_message_area();
                }
            }});
    }

    function clear_message_area() {
        $(".current-msg-length").text(MAX_LENGTH);
        $("#message-area").val('');
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

    // Initializing "how it works" stuff
    audience_how_it_works_spinning_gears_setup();

    $('div[rel]').overlay({
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


  var msg_area = $("textarea[name=message]");
  if(msg_area[0]){
	msg_area[0].onkeydown = msg_area[0].onkeyup = (function() {
    	$(".current-msg-length").text(MAX_LENGTH-msg_area.val().length);
    	if (msg_area.val().length > MAX_LENGTH) {
      		$("#send_comment").enable(false);
      		msg_area.addClass("error");
    	} else {
      		$("#send_comment").enable(true);
      		msg_area.removeClass("error");
    	}
  	});
  }
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

function showEncaminhada(parentId) {
    $('#encaminhada-' + parentId).slideToggle();
}
