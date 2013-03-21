/*
  jQuery Long Poll plugin 0.0.1 (02-05-2010)

  Copyright (c) 2010 JavaScript Guy

  This script is licensed as free software under the terms of the
  LGPL License: http://www.opensource.org/licenses/lgpl-license.php
*/
( function ( $)
  {
    $.longPoll = function ( args)
                 {
                   args = args || {};
                   var self = $.extend (
                              {
                                url: '',                        // URL To connect to
                                reconnect: true,                // If we're automatically reconnecting
                                errorTimeout: 30,               // Timeout for errors, eg: server timeout, execution time limit, etc.
                                errorTimeoutDelay: .5,          // Seconds to delay, if the connection failed in an error
                                hasConnection: false,           // If we have a connection
                                etag: 0,
                                last_modified: 'Thu, 1 Jan 1970 00:00:00 GMT',
                                error: false,
                                request: null,

                                // Function to handle reconnections:
                                reconnectFunc: function ()
                                               {
                                                 if ( self.reconnect)
                                                 {
                                                   self.disconnect ();
                                                   // Reconnect - with longer error timeout delay (in case we have an intermittent connection)
                                                   if ( self.error)
                                                   {
                                                     setTimeout ( function ()
                                                                  {
                                                                    self.connect ();
                                                                  },
                                                                  self.errorTimeoutDelay * 1000
                                                                );
                                                   } else {
                                                     self.connect ();
                                                   }
                                                 }
                                               },

                                // Function to create new connection:
                                connect: function ()
                                         {
                                           self.reconnect = true;
                                           self.request = $.ajax (
                                                          {
                                                            url: self.url,
                                                            async: true,
                                                            cache: false,
                                                            dataType: 'text',
                                                            type: 'GET',
                                                            timeout: self.errorTimeout * 1000,              // Timeout and reconnect
                                                            beforeSend: function ( XHR)
                                                            {
                                                              XHR.setRequestHeader ( 'If-None-Match', self.etag);
                                                              XHR.setRequestHeader ( 'If-Modified-Since', self.last_modified);
                                                            },
                                                            error: function ( XHR, textStatus, errorThrown)
                                                            {
                                                              self.reconnectFunc ();
                                                              self.error = true;
                                                            },
                                                            success: function ( data, textStatus, XHR)
                                                            {
                                                              self.etag = XHR.getResponseHeader ( 'Etag');
                                                              self.last_modified = XHR.getResponseHeader ( 'Last-Modified');
                                                              self.success ( data);
                                                              self.error = false;
                                                            },
                                                            complete: function ( data)
                                                            {
                                                              self.reconnectFunc ();
                                                            }
                                                          });
                                           self.hasConnection = true;
                                         },

                                // Function to abort long pooling:
                                disconnect: function ()
                                            {
                                              self.reconnect = false;
                                              if ( self.request)
                                              {
                                                self.request.abort ();
                                              }
                                              self.hasConnection = false;
                                            },

                                // Function to handle data when received:
                                success: function ( data)
                                         {
                                         }
                              }, args);
                   return self;
                 };
  }) (jQuery);