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



