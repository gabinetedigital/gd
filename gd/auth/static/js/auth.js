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

        /** Configuring the DOM element that holds the login form */
        , $loginOverlay: $('#loginoverlay').overlay({
            api: true,
            mask: {
                color: '#333',
                opacity: 0.8
            },
            oneInstance: false,
            speed: 'fast',
            onBeforeLoad: function() {
                var wrap = this.getOverlay().find(".contentWrap");
                wrap.load(url_for('auth.login'));
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

                    $.post(url_for('auth.login_json'), params, function (data) {
                        var pData = $.parseJSON(data);
                        if (pData.status !== 'ok') {
                            overlay.find('div.error').html(pData.msg).fadeIn('fast');
                        } else {
                            closeMethod();
                            auth.userAuthenticated(pData.msg.user);
                        }
                    });
                    return false;
                });
            }
        })

        /** Configuring the DOM element that holds the signup form */
        , $signOverlay: $('#signupoverlay').overlay({
            api: true,
            fixed: false,
            mask: {
                color: '#333',
                opacity: 0.8
            },
            oneInstance: false,
            speed: 'fast',
            onBeforeLoad: function() {
                var wrap = this.getOverlay().find(".contentWrap");
                wrap.load(url_for('auth.signup'));
            },
            onLoad: function() {
                var overlay = this.getOverlay();
                var closeMethod = this.close;

                /* focus the name field */
                overlay.find('input[name=name]').focus();

                $(overlay.find('form')).ajaxForm({
                    beforeSubmit: function () {
                        /* Maybe it's not the first time the user is
                         * trying to send the form, let's clear the
                         * error state for now to allow him to try
                         * again */
                        overlay.find('input,select').removeClass('error');
                    },

                    success: function (data) {
                        var pData = $.parseJSON(data);
                        if (pData.status === 'ok') {
                            closeMethod();
                            auth.userAuthenticated(pData.msg.user);
                            return;
                        }

                        /* Here we're sure that things didn't work :( */
                        var errors = pData.msg.data;
                        var code = pData.code;
                        var csrfToken = pData.msg.csrf;

                        /* The first step now is to set the new csrf token to
                         * our form. If we don't do it, we can't try to
                         * register again. */
                        overlay.find('[name=csrf]').val(csrfToken);

                        /* The user made a mistake when filling the form */
                        if (code === 'ValidationError') {
                            for (var f in errors) {
                                overlay
                                    .find('[name=' + f  + ']')
                                    .addClass('error');
                            }
                        } else {
                            console.debug(pData);
                            overlay
                                .find('div.error')
                                .html(pData.msg.data).fadeIn('fast');
                        }
                    }
                });
            }
        })

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
            this.$loginOverlay.load();
            if (params && typeof params.success === 'function') {
                this.success = params.success;
            }
            return false;
        }

        /** Shows the signup form */
        , showSignupForm: function (params) {
            this.$signOverlay.load();
            return false;
        }

        /** Method called after a successful authentication. It saves
         *  the authentication information and makes sure that the user
         *  interface will be updated showing authentication info. */
        , userAuthenticated: function (user) {
            this.user = user;
            this.success();
            this.updateLoginWidget();
        }

        /** This method updates the login widget to show links that
         *  only makes sense to be shown after logged in or logged out */
        , updateLoginWidget: function () {
            $('ul.login li').fadeOut('slow', function () {
                var $ul = $('ul.login');
                var template = (auth.isAuthenticated() ? 'loggedin' : 'loggedout');
                template += 'Template';
                $ul.html('');
                $(tmpl(template, auth.user || {})).appendTo($ul);
            });
        }

        /** Logs the user out */
        , logout: function () {
            $.get(url_for('auth.logout_json'), function () {
                auth.user = null;
                auth.updateLoginWidget();
            });
        }

        /** Method called in the login form, by the user that is not
         *  yet signed up to our site */
        , swapLoginToSignup: function () {
            this.$loginOverlay.close();
            window.parent.setTimeout(function () {
                auth.showSignupForm();
            }, 300);
        }
    };

    return new Auth();
})();
