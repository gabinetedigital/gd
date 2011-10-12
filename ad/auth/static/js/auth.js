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

/* Namespace for authentication stuff */
var auth = (function() {

    /** Class that unifies the main things about authentication */
    function Auth() { }

    Auth.prototype = {
        /** Place to store cached authentication data. Actually, the
         * whole authenticated user information. */
        user: null

        /** Callback that will be fired after a successful
         *  authentication */
        , success: function () {}

        /** Returns True if there is someone authenticated */
        , isAuthenticated: function () {
            return this.user !== null;
        }

        /** Returns the current authenticated user */
        , authenticatedUser: function () {
            return this.user;
        }

        /** Shows the login form and register callbacks to be called when
         *  it returns successfuly or not */
        , showLoginForm: function (params) {
            $('a[rel=#loginoverlay]').click();
            if (typeof params.success === 'function') {
                this.success = params.success;
            }
        }

        /** Method called after a successful authentication. It saves
         *  the authentication information and makes sure that the user
         *  interface will be updated showing authentication info. */
        , userAuthenticated: function (user) {
            this.user = user;
            this.success();
        }
    };

    /* Overlay for all <a> tags with a `rel' attribute */
    $('a[rel=#loginoverlay]').overlay({
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
                        overlay.find('div.error').html(data.msg).fadeIn('fast');
                    } else {
                        closeMethod();
                        auth.userAuthenticated(data.msg.user);
                    }
                });
                return false;
            });
        }
    });

    return new Auth();
})();
