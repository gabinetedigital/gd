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
    /* Overlay for all <a> tags with a `rel' attribute */
    $('a[rel]').overlay({
        top: 250,
        mask: {
            color: '#fff',
            opacity: 0.5
        },
        oneInstance: false,
        speed: 'fast',
        onBeforeLoad: function() {
	    var wrap = this.getOverlay().find(".contentWrap");
	    wrap.load(this.getTrigger().attr("href"));
	},
        onLoad: function() {
            var overlay = this.getOverlay();
            var closeMethod = this.close;

            /* Just focus the username when overlay shows up */
            overlay.find('input[name=username]').focus();

            /* The submit button does its miracles of cancelling the usual
             * form submit and send data via ajax */
            overlay.find('form').submit(function () {
                var params = {
                    username: overlay.find('input[name=username]').val(),
                    password: overlay.find('input[name=password]').val()
                };

                $.getJSON(url_for('auth.login_json'), params, function (data) {
                    if (data.status !== 'ok') {
                        overlay.find('input[type!=submit]').css(
                            'border', 'solid 1px #e00');
                    } else {
                        closeMethod();
                    }
                });
                return false;
            });
        }
    });
});
