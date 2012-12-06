/* Copyright (C) 2012  Guilherme Guerra <guerrinha@comum.org>
 * Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Guilherme Guerra <guerrinha@comum.org>
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

$(document).ready(function() {

    $('.fancybox img').resizecrop({
      width:200,
      height:200,
    });

    $(".fancybox").fancybox({
        // beforeShow: function () {
        //     if (this.title) {
        //         this.title += '<br>';
        //         this.title += '<div class="share">';
        //         this.title += '<span class="st_facebook_hcount" displayText="Facebook"></span>';
        //         this.title += '<span class="st_twitter_hcount" displayText="Tweet"></span>';
        //         this.title += '<span class="st_plusone_hcount" displayText="Google +1"></span>';
        //         this.title += '</div>';
        //     }
        // },
        beforeShow: function () {
            var $download = $(this.element).attr('data-download');
            if (this.title) {
                this.title += '<br>';

                this.title += '<a href="'+$download+'" class="btn btn-danger pull-right hidden-phone">Download original</a>';
            }
        },
    	openEffect	: 'elastic',
    	closeEffect	: 'elastic',
        helpers		: {
	    title	: { type : 'inside' },
	}
    });

    function pageload(hash) {
        // hash doesn't contain the first # character.
        if(hash) {
            $.galleriffic.gotoImage(hash);
        } else {
            gallery.gotoIndex(0);
        }
    };
    $.historyInit(pageload, { unescape: ",/" } );

    $('#slideshow > img').hide();
    $('.prev').addClass('awesome');
    $('.next').addClass('awesome');
    $('.play').hide();

});
