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

$(function () {

    $("#show-hidden").click(function(ev) { //like twitter 'more' button
        ev.preventDefault();
        hidden_count = 0;
        $("#show-hidden").hide();
        $('.listing li').slideDown();
    });

    $("#suggested-notices").click(function(ev)  {
        ev.preventDefault();
        $("#second-listing").hide();
        $("#main-listing").show();
    });

    $("#published-notices").click(function(ev) {
        ev.preventDefault();
        $("#second-listing").show();
        $("#second-listing a").hide(); //hide buttons of already published
        $("#main-listing").hide();
    });

    $("#new-notices").click(function(ev)  {
        ev.preventDefault();
        $("#new-notices").addClass('selected');
        $("#accepted-notices").removeClass('selected');

        $("#second-listing").hide();
        $("#main-listing").show();
    });

    $("#accepted-notices").click(function(ev) {
        ev.preventDefault();
        $("#new-notices").removeClass('selected');
        $("#accepted-notices").addClass('selected');

        $("#second-listing").show();
        $("#second-listing a").hide(); //hide buttons of already published
        $("#main-listing").hide();
    });

    /* Binding the click of the `control' links to an ajax get instead
     * of letting the whole page redirect/update. */
    function updateToAjax () {
        var $a = $(this);
        $.getJSON($(this).attr('href'), function (data) {
            if (data.status === 'ok') {
                var li = $a
                    .parent() // div.controls
                    .parent(); // li
                li.slideUp(function() {
                    li.remove();
                });
            }
        });
        return false;
    }
    $('div.controls a').click(updateToAjax);

    var hidden_count = 0;
    var is_first_update = true;

    /* Creates a new instance of the buzz machinery that automatically
     * updates the buzz list. */
    function updateBuzz(msg, ul) {
        var $el = $(tmpl("buzzTemplate", msg));
        $('div.controls a', $el).click(updateToAjax);

        if (!is_first_update) {
            $el.hide();
            hidden_count++;
            $("#show-hidden").text("("+hidden_count + " new)");
            $("#show-hidden").show();
        }
        ul.prepend($el);
    }

    function is_moderated_page() {
        return location.href.indexOf('moderate') >= 0;
    }

    function is_publish_page() {
        return location.href.indexOf('publish') >= 0;
    }

    new Buzz(BASE_URL,{
        new_buzz: function (msg) {
            if (is_moderated_page()) {
                updateBuzz(msg, $('#main-listing'));
            }
        },
        buzz_accepted: function (msg) {
            if (is_moderated_page()) {
              updateBuzz(msg, $('#second-listing'));
            }
        },
        buzz_selected: function (msg) {
            if (is_publish_page()) {
              updateBuzz(msg, $('#main-listing'));
            }
        },
        buzz_published: function (msg) {
            if (is_publish_page()) {
              updateBuzz(msg, $('#second-listing'));
            }
        },
        done: function() {
            is_first_update = false;
            $("#listing-loading").remove();
        }
    });
});
