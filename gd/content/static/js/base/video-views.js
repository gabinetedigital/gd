/* Copyright (C) 2011  Sergio Berlotto Jr <sergio.berlotto@gmail.com>
 * Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Sergio Berlotto Jr <sergio-berlotto@sgg.rs.gov.br>
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

$(window).load(function() {

  $('video').mediaelementplayer({
      success: function(media, node, player) {
          media.addEventListener('play', function(e) {
            var vid = $('video').attr('data-vid');
            var ck  = 'pv'+vid
            if(!$.cookie(ck) ){
                $.post('/videos/'+vid+'/mv');
            }
            $.cookie(ck, true, { expires: 365 });
          });
      }
  });

});
