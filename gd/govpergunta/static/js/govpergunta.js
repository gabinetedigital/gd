var navapi = null;

$(function () {
    var wizard = $('.wizard').data('isLoaded', false);

    $('#maintext, .tabs').click(function() {
        wizard.expose({ color:'#ddd', lazy:true });
        $('html,body').animate({ scrollTop: 320 }, 150);
    });

    $("ol.tabs", wizard).tabs(
        "div.panes > div", {
            effect: 'fade',
            lazy: true,
            onBeforeClick: function () {
                if (wizard.data('isLoaded')) {
                    $('html,body').animate({ scrollTop: 320 }, 150);
                }
            }
        });
    wizard.data('isLoaded', true);

    navapi = $("ol.tabs", wizard).data("tabs");

    // "next tab" button
    $(".next", wizard).click(function () {
        $('html,body').animate({ scrollTop: 320 }, 100);
	navapi.next();
    });

    // "previous tab" button
    $(".prev", wizard).click(function () {
        $('html,body').animate({ scrollTop: 320 }, 100);
	navapi.prev();
    });
});
