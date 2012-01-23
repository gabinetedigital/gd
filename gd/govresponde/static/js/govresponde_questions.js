/* Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
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

function showAggregated(parentId) {
    $('#aggregated-' + parentId).slideToggle();
}

function vote(qid) {
    $.get(url_for('govresponde.vote.<qid>', { qid: qid }), function (data) {
        $('#question-' + qid + ' button').replaceWith(
            $('<div>')
                .addClass('success')
                .addClass('msg')
                .show()
                .html('Obrigado por votar. Seu voto foi contabilizado'));
        $('#question-' + qid + ' .score')
            .fadeOut(function () {
                $(this)
                    .html(data)
                    .fadeIn();
            });
    });
}
