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

// Inicia longpool
var buzz_longpool = $.longPoll (
    {
      url: '/buzz/sub?id=' + window.AUDIENCE_ID,
      success: function ( data)
      {
    	try {
    	  data = $.parseJSON ( data);
    	} catch ( e) {}
        if ( data.type)
        {
          if ( data.type == 'published')
          {
            $('#beingAnswered').fadeOut ().html ( '<ul class="stream"><li class="avatar"><img src="' + data.avatar + '"></li><li class="author">' + data.author + ' <em>| ' + data.authortype + '</em></li><li class="answer">' + data.content + '</li></ul>').fadeIn ();
          }
          if ( data.type == 'moderated' || data.type == 'public')
          {
            $('#buzz-' + data.type).prepend ( '<li><ul class="stream"><li class="avatar"><img src="' + data.avatar + '"></li><li class="author">' + data.author + ' <em>| ' + data.authortype + '</em></li><li class="answer">' + data.content + '</li></ul></li>').fadeIn ();
          }
        }
      }
    });
setTimeout ( buzz_longpool.connect, 0);