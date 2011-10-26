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

$(document).ready(function () {
    $('.carousel').jcarousel({
        scroll: 1,
        auto: 5,
        wrap: 'last',
        buttonNextHTML: null,
        buttonPrevHTML: null,
        initCallback: function (carousel) {
            $('.controls a[href=#1]').addClass('selected');

            $('.controls a').bind('click', function() {
                // Actually selecting the current item
                var pos = $(this).attr('href').replace('#', '');
                carousel.scroll($.jcarousel.intval(pos));
                return false;
            });
        },

        itemVisibleInCallback: function (carousel, item, idx, state) {
            $('.controls a').removeClass('selected');
            $('.controls a[href=#' + (idx) +']').addClass('selected');
        }
    });
});
