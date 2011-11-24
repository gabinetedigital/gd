$(function() {
  $("#option_1").click(function(ev) {
    ev.preventDefault();
    $("#vote-direction").attr("value", "left");
    $("#vote-form").submit();
  });

  $("#option_2").click(function(ev) {
    ev.preventDefault();
    $("#vote-direction").attr("value", "right");
    $("#vote-form").submit();
  });

  $("#vote-skip").click(function(ev) {
    ev.preventDefault();
    $("#vote-direction").attr("value", "skip");
    $("#vote-form").submit();
  });
});
