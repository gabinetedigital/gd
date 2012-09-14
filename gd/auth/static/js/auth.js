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

        // , $loginOverlay: $('#loginoverlay').overlay({
        //     api: true,
        //     top: '5px',
        //     oneInstance: false,
        //     speed: 'fast',
        //     mask: {
        //         color: '#111',
        //         opacity: 0.7
        //     },
        //     onBeforeLoad: function() {
        //         var overlay = this.getOverlay();
        //         var wrap = overlay.find(".contentWrap");
        //         var closeMethod = this.close;
        //         wrap.load(url_for('auth.login'), function () {
        //             /* Just focus the username when overlay shows up */
        //             overlay.find('input[name=username]').focus();

        //             /* We're done! */
        //             overlay.removeClass('loading');

        //             $(overlay.find('form')).ajaxForm({
        //                 beforeSubmit: function () {
        //                     $('.msg').fadeOut();
        //                 },

        //                 success: function (data) {
        //                     var pData = $.parseJSON(data);
        //                     if (pData.status !== 'ok') {
        //                         overlay
        //                             .find('#auth-error')
        //                             .html(pData.msg)
        //                             .fadeIn('fast');
        //                     } else {
        //                         closeMethod();
        //                         auth.userAuthenticated(pData.msg.user);
        //                     }
        //                     return false;
        //                 }
        //             });

        //             overlay.find('#remember_password').ajaxForm({
        //                 beforeSubmit: function () {
        //                     overlay.find('.msg').fadeOut();
        //                 },

        //                 success: function (data) {
        //                     var pData = $.parseJSON(data);
        //                     if (pData.status !== 'ok') {
        //                         overlay
        //                             .find('#remember-password-error')
        //                             .html(pData.msg)
        //                             .fadeIn('fast');
        //                         overlay
        //                             .find('#remember-password-success')
        //                             .hide();
        //                     } else {
        //                         overlay
        //                             .find('#remember-password-success')
        //                             .html(pData.msg)
        //                             .fadeIn('fast');
        //                         overlay
        //                             .find('#remember-password-error')
        //                             .hide();
        //                         overlay.find('input[name=email]').val('');
        //                     }
        //                     window.setTimeout(function () {
        //                         overlay.find('.msg').fadeOut();
        //                     }, 10000);
        //                 }
        //             });
        //         });
        //     }
        // })

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
//            this.$signOverlay.load();
            //alert(':'+url_for('auth.signup'));
            options = {
                keyboard: true,
                show: true,
                remote: url_for('auth.signup')
            };
            $('#myModal').modal(options);


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
            if( auth.isAuthenticated() ){
                $('.logado').show();
                $('.off').hide();
                $('.on').hide();
            }else{
                $('.logado').hide();
                $('.off').show();
                $('.on').hide();
            }
        }

        /** Logs the user out */
        , logout: function () {
            $.get(url_for('auth.logout_json'), function () {
                auth.user = null;
                auth.updateLoginWidget();
                //$(".comment-error").show();
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
            var $lgForm = $('div.on');

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
