/* Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
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

function changeCurrentPic(link) {
    var $link = $(link);

    /* Resseting the css class */
    $('ul.images li a').removeClass('selected');
    $link.addClass('selected');

    /* Loading the new text and picture */
    $('#currentgallery .currentpic p').html($link.attr('title'));
    $('#currentgallery .currentpic img')
        .attr('src', '')
        .attr('src', $link.attr('href'));

    /* Moving the focus to the top of the image */
    $('html,body').animate({ scrollTop: 270 }, 100);
    return false;
}


function nextPic() {
    var link = $('ul.images li a.selected').parent().next().find('a');
    changeCurrentPic(link);
}


function prevPic() {
    var link = $('ul.images li a.selected').parent().prev().find('a');
    changeCurrentPic(link);
}
