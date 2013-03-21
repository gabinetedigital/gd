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


    $('.overlayt').attr('rel', function () {
        return $(this).attr('href');
    }).overlay({
        oneInstance: false,
        speed: 'fast',
        mask: {
            color: '#111',
            opacity: 0.7
        },
        onBeforeLoad: function() {
            var overlay = this.getOverlay();
            var wrap = overlay.find(".contentWrap");
            var closeMethod = this.close;
            var url =
                    url_for('pages.govpergunta.como-funciona-a-votacao') +
                    '.json';
            $.getJSON(url, function (data) {
                /* We're done! */
                overlay.removeClass('loading');

                /* Loading the content */
                wrap.html(data.content);
            });
        }
    });


    $('#voteswarn').overlay({
        load: true,
        oneInstance: false,
        closeOnClick: false,
        speed: 'fast',
        mask: {
            color: '#111',
            opacity: 0.7
        }
    });
});
