/* Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
 *
 *   Author: Rodrigo Sebastiao da Rosa <rodrigo-rosa@procergs.rs.gov.br>
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

$(function () {
    function removeSourceFormat() {
	$(".deleteSourceFormat").unbind("click");
	$(".deleteSourceFormat").bind("click", function () {
	    i=0;
	    $("p.sourceFormat").each(function () {
		i++;
	    });
	    if (i>1) {
		$(this).parent().remove();
	    }
	});
    }
    removeSourceFormat();
    $("#addSourceFormat").click(function () {
	newLine = $("p.sourceFormat:first").clone();
	newLine.find("input").val("");
	newLine.insertAfter("p.sourceFormat:last");
	removeSourceFormat();
    });
    function removeTerm() {
	$(".deleteTerm").unbind("click");
	$(".deleteTerm").bind("click", function () {
	    i=0;
	    $("p.listTerm").each(function () {
		i++;
	    });
	    if (i>1) {
		$(this).parent().remove();
	    }
	});
    }
    removeTerm();
    $("#addTerm").click(function () {
	newLine = $("p.listTerm:first").clone();
	newLine.find("input").val("");
        newLine.find("input[type=text]").change(function(){
            $(this).parent().find("input[type=radio]").val($(this).val());
        });
        newLine.insertAfter("p.listTerm:last");
	removeTerm();
        nameRadio();
    });
    function nameRadio(){
        $("p.listTerm").find("input[type=text]").change(function(){
            $(this).parent().find("input[type=radio]").val($(this).val());
        });
    }
    nameRadio();

});
