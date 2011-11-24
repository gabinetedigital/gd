$(function() {
  $("#option_1").click(function(ev) {
    ev.preventDefault()
    $.ajax({
      type:'post',
      url: url_for('govpergunta.add_vote'),
      data: {direction:'left', token:VOTE_TOKEN},
      error: function(e) {
        // console.log("error 1")
        // console.dir(e)
          },
      success: function(data) {
        document.location.reload()
      }
    });
  });

  $("#option_2").click(function(ev) {
    ev.preventDefault()
    $.ajax({
      type:'post',
      url: url_for('govpergunta.add_vote'),
      data: {direction:'right', token:VOTE_TOKEN},
      error: function(e) {
        // console.log("error 1")
        // console.dir(e)
          },
      success: function(data) {
        document.location.reload()
      }
    });
  });
});
