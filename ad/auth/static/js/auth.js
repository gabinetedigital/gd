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


$(function() {
    $('a[rel]').overlay({
        top: 250,
        mask: 'gray',
        oneInstance: false,
        speed: 'fast',
        onBeforeLoad: function() {
	    var wrap = this.getOverlay().find(".contentWrap");
	    wrap.load(this.getTrigger().attr("href"));
	},
        onLoad: function() {
            this.getOverlay().find('input[name=username]').focus();
        }
    });
});
