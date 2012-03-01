/* Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
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

    var onload_callback = null;

    Auth.prototype = {
        /** Place to store cached authentication data. Actually, the
         * whole authenticated user information. */
        user: null

        /** Configuring the DOM element that holds the login form */
        , $loginOverlay: $('#loginoverlay').overlay({
            api: true,
            top: '5px',
            oneInstance: false,
            speed: 'fast',
            mask: {
                color: '#111',
                opacity: 0.7
            },
            onBeforeLoad: function() {
                var overlay = this.getOverlay();
                var wrap = overlay.find(".contentWrap");
                var closeMethod = this.close;
                wrap.load(url_for('auth.login'), function () {
                    /* Just focus the username when overlay shows up */
                    overlay.find('input[name=username]').focus();

                    /* We're done! */
                    overlay.removeClass('loading');

                    $(overlay.find('form')).ajaxForm({
                        beforeSubmit: function () {
                            $('.msg').fadeOut();
                        },

                        success: function (data) {
                            var pData = $.parseJSON(data);
                            if (pData.status !== 'ok') {
                                overlay
                                    .find('#auth-error')
                                    .html(pData.msg)
                                    .fadeIn('fast');
                            } else {
                                closeMethod();
                                auth.userAuthenticated(pData.msg.user);
                            }
                            return false;
                        }
                    });

                    overlay.find('#remember_password').ajaxForm({
                        beforeSubmit: function () {
                            overlay.find('.msg').fadeOut();
                        },

                        success: function (data) {
                            var pData = $.parseJSON(data);
                            if (pData.status !== 'ok') {
                                overlay
                                    .find('#remember-password-error')
                                    .html(pData.msg)
                                    .fadeIn('fast');
                                overlay
                                    .find('#remember-password-success')
                                    .hide();
                            } else {
                                overlay
                                    .find('#remember-password-success')
                                    .html(pData.msg)
                                    .fadeIn('fast');
                                overlay
                                    .find('#remember-password-error')
                                    .hide();
                                overlay.find('input[name=email]').val('');
                            }
                            window.setTimeout(function () {
                                overlay.find('.msg').fadeOut();
                            }, 10000);
                        }
                    });
                });
            }
        })

        /** Configuring the DOM element that holds the signup form */
        , $signOverlay: $('#signupoverlay').overlay({
            api: true,
            fixed: false,
            top: '5px',
            mask: {
                color: '#333',
                opacity: 0.8
            },
            oneInstance: false,
            speed: 'fast',
            onBeforeLoad: function() {
                var wrap = this.getOverlay().find(".contentWrap");
                var overlay = this.getOverlay();
                var closeMethod = this.close;

                wrap.load(url_for('auth.signup'), function () {
                    /* focus the name field */
                    overlay.find('input[name=name]').focus();

                    $(overlay.find('form')).ajaxForm({
                        beforeSubmit: function () {
                            /* Maybe it's not the first time the user is
                             * trying to send the form, let's clear the
                             * error state for now to allow him to try
                             * again */
                            overlay.find('input,select').removeClass('fielderror');
                            overlay.find('.errmsg').html('').hide();
                        },

                        success: function (rdata) {
                            var data = $.parseJSON(rdata);

                            if (data.status === 'ok') {
                                closeMethod();
                                auth.feedbackAfterSignup();
                                return;
                            }

                            /* Here we know that something is wrong */
                            var form = overlay.find('form');
                            var code = data.code;
                            var errors = data.msg;

                            /* Just updating this object with received data */
                            if (data.msg.data)
                                errors = data.msg.data;

                            /* The first step now is to set the new csrf
                             * token to our form. If we don't do it, we
                             * can't try to register again. */
                            if (data.msg.csrf !== undefined)
                                form.find('[name=csrf]').val(data.msg.csrf);

                            /* The user made a mistake when filling the form */
                            if (code === 'ValidationError') {
                                for (var f in errors) {
                                    overlay
                                        .find('[name=' + f  + ']')
                                        .addClass('fielderror');
                                    overlay
                                        .find('.'+ f + '-error')
                                        .html(errors[f][0])
                                        .show();
                                }
                            } else {
                                overlay
                                    .find('div.error')
                                    .fadeIn()
                                    .html(errors);
                            }
                        }
                    });
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
                $(".comment-error").show();
                if (window.location.href.indexOf('profile') > 0) {
                    window.location.href = INDEX_URL;
                }
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

        /** Toggles the visibility of the "password reminder" screen in
         *  the login form */
        , togglePasswordReminder: function () {
            var $prForm = $('div.passwordReminder');
            var $lgForm = $('div.loginForm');

            if ($lgForm.is(':visible')) {
                $lgForm.fadeOut('fast', function () {
                    $prForm.fadeIn();
                    $prForm.find('input[name=email]').focus();
                });
            } else {
                $prForm.fadeOut('fast', function () {
                    $lgForm.fadeIn();
                    $lgForm.find('input[name=username]').focus();
                });
            }
        }

        /** Toggles tabs of the signup overlay (readmore, tos, form) */
        , toggleSignupTab: function (tabName) {
            var $target = $('div.tab.' + tabName);
            if (!$target.is(':visible')) {
                $('div.tab').each(function () {
                    if (!$(this).hasClass(tabName)) {
                        $(this).fadeOut(200);
                    }
                });
                window.setTimeout(function () {
                    $target.fadeIn();
                }, 200);
            }
        }

        /** Shows a box with a feedback to the user after user's signup */
        , feedbackAfterSignup: function () {
            var $overlay = $('#signupfeedback').overlay({
                api: true,
                top: '10px',
                oneInstance: false,
                speed: 'fast',
                left: '60%'
            });

            $overlay.load();
            window.setTimeout(function () {
                $overlay.close();
            }, 8000);
        }
    };

    return new Auth();
})();
