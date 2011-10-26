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

function url_for(base, params) {
    var url = BASE_URL;
    $(base.split('.')).each(function (index, item) {
        if (item.charAt(0) === '<') {
            item = params[item.replace(/^\<([^>]+)\>/, '$1')];
        }
        url += item + '/';
    });

    if (url.charAt(url.length-1) === '/') {
        url = url.substr(0, url.length-1);
    }
    return url;
}
