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
            fixed: true,
            top: '10%',
            mask: {
                color: '#333',
                opacity: 0.8
            },
            oneInstance: false,
            speed: 'fast',

            alternativeUrl: '',
            onBeforeLoad: function() {
                var wrap = this.getOverlay().find(".contentWrap");
                var overlay = this.getOverlay();
                var closeMethod = this.close;
                if(this.alternativeUrl){
                    wrap.load(this.alternativeUrl);
                }else{
                    wrap.load(url_for('auth.signup') + '?readmore');
                }



            }
        })

        /** Callback that will be fired after a successful
         *  authentication */
        , success: function () {}

        , callback_login: function (action) {}

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
            $('.off').hide();
            $('.on').fadeIn(function(){
                $('#username').focus();
            });
            return false;
        }

        /** Shows the signup form */
        , showSignupForm: function (params) {
            if( params && params['directToForm'] || params == 'directToForm' ){
                this.$signOverlay.alternativeUrl = url_for('auth.signup');
            }
            this.$signOverlay.load();
            //alert(':'+url_for('auth.signup'));

            //$('#signupoverlay .contentWrap .ct').load(url_for('auth.signup') + '?readmore');

            return false;
        }

        /** Toggles tabs of the signup overlay (readmore, tos, form) */
        , toggleSignupTab: function (tabName) {
            var wrap = $('#signupoverlay').find(".contentWrap");
            if(tabName == 'tos'){
                wrap.load(url_for('auth.signup') + '?tos');
            }else if (tabName == 'readmore'){
                wrap.load(url_for('auth.signup') + '?readmore');
            }else{
                wrap.load(url_for('auth.signup'), function(){
                    $($('#signupoverlay').find('form')).ajaxForm({
                        beforeSubmit: function () {
                            $('.errmsg').fadeOut();
                            $('#auth-error').fadeOut();
                        },

                        success: function (data) {
                            var pData = $.parseJSON(data);
                            if (pData.status !== 'ok') {
                                $('#auth-error').html('Corrija os campos abaixo').fadeIn('fast');
                                if( typeof pData.msg.data==="string" ){
                                    $('#auth-error').html(pData.msg.data).fadeIn('fast');
                                }else{
                                    for(campo in pData.msg.data){
                                        $('#signupoverlay')
                                            .find('.'+campo+'-error')
                                            .html( pData.msg.data[campo][0] )
                                            .fadeIn('fast');

                                    }
                                }
                            } else {
                                $('#auth-success')
                                   .html('Obrigado! Agora siga os passos no email que você recebeu para concluir seu cadastro.')
                                   .fadeIn('fast');
                                $('#signupoverlay').scrollTop();
                                //auth.close();
                                //auth.userAuthenticated(pData.msg.user);
                                $('#signupoverlay').find('form').fadeOut('fast');
                            }
                            return false;
                        }
                    });
                });

            }
        }

        /** Method called after a successful authentication. It saves
         *  the authentication information and makes sure that the user
         *  interface will be updated showing authentication info. */
        , userAuthenticated: function (user) {
            this.user = user;
            this.success();
            if(auth.callback_login && typeof auth.callback_login === 'function'){
                auth.callback_login('login');
            }
            this.updateLoginWidget();
        }

        /** This method updates the login widget to show links that
         *  only makes sense to be shown after logged in or logged out */
        , updateLoginWidget: function () {
            if( auth.isAuthenticated() ){
                $('.logado').show();
                $('.off').hide();
                $('.on').hide();
                $('.saudacao').html('Olá, ' + this.user.display_name + '!');
            }else{
                $('.saudacao').html('Olá, Visitante!');
                $('.logado').hide();
                $('.off').show();
                $('.on').hide();
            }
        }

        /** Logs the user out */
        , logout: function () {
            $.get(url_for('auth.logout_json'), function () {
                auth.user = null;
                if(auth.callback_login && typeof auth.callback_login === 'function'){
                    auth.callback_login('logout');
                }
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
