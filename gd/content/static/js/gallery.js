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

    // Initialize Minimal Galleriffic Gallery
    $('#thumbs').galleriffic({
        imageContainerSel:      '#slideshow',
        controlsContainerSel:   '#controls',
        captionContainerSel:    '#caption',
        numThumbs:                 10,
        maxPagesToShow:            20,
        prevLinkText:              '«',
        nextLinkText:              '»',
        nextPageLinkText:          '>',
        prevPageLinkText:          '<',
        onTransitionIn: function(slide, caption, isSync) {
            var duration = this.getDefaultTransitionDuration(isSync);
            var slideImage = slide.find('img');
            slide.fadeTo(duration, 1.0);

            caption.width(slideImage.width())
                .css({
                    'bottom' : ($('#caption').height()+3),
                    'left' : ((Math.floor(($('#slideshow').width() - slideImage.width()) / 2) + 2 )),
                })

            $('#caption span.image-caption').fadeTo(1000, 0.8);
        },
    });


    $('#slideshow > img').hide();
    $('.prev').addClass('awesome');
    $('.next').addClass('awesome');
    $('.play').hide();



});