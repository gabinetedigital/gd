/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
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

var video = (function () {
    function Video() {
        this.playingVideo = null;
    }

    function _getOverlay() {
        var $el = $('#videoOverlay');
        if ($el.length === 0) {
            return $('<div>')
                .attr('id', '#videoOverlay')
                .addClass('overlay')
                .addClass('video')
                .append($('<div>').addClass('contentWrap'))
                .appendTo($('body'));
        }
        return $el;
    }

    Video.prototype = {
        $loginOverlay: _getOverlay().overlay({
            api: true,
            mask: {
                color: '#111',
                opacity: 0.7
            },
            oneInstance: false,
            speed: 'fast',
            onBeforeLoad: function() {
                var wrap = this.getOverlay().find('.contentWrap');
                var id = video.playingVideo.id;
                $(tmpl('videoTemplate', video.playingVideo)).appendTo(wrap);
                $('<video>')
                    .attr('id', id)
                    .attr({width:490, height:290})
                    .appendTo(wrap.find('.videoContainer'));
                avl.loadPlayers();
            },

            onLoad: function() {
            },

            onClose: function () {
                this.getOverlay().find('.contentWrap').html('');
            }
        })

        , play: function (video) {
            this.playingVideo = video;
            this.$loginOverlay.load();
        }
    };

    return new Video();
})();

/* Called by the embed link in a video overlay */
function toggleEmbed(obj) {
    $('.overlay.video textarea').slideToggle();
}
