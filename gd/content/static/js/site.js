$(function () {

  $("#participe .govresponde")
        .data('text','Quer saber o que o Governador pensa? Pergunte para ele. ' +
              'A questão mais votada do mês é respondida em vídeo.');
  $("#participe .govpergunta")
        .data('text', 'O Governador pergunta e a sociedade responde com novas ' +
              'idéias.');
  $("#participe .agenda")
        .data('text', 'Quer fazer parte da agenda do Governador na sua cidade?' +
              ' Indique uma pauta na agenda colaborativa.');
  $("#participe .govescuta")
        .data('text','Audiências públicas digitais transmitidas via internet  ' +
              'onde você pode enviar sua contribuição.');
  $("#participe").mouseenter(function() {
    if (home_menu_delay) clearTimeout(home_menu_delay);
  });

  $("#participe").mouseleave(prepare_to_hide_home_menu);

  var home_menu_delay;
  function show_home_menu() {
    if (home_menu_delay) {
      clearTimeout(home_menu_delay);
    } else {
      $("#slideshow").slideUp();
      $("#participe").slideDown();
    }
  }

  function hide_home_menu() {
    $("#slideshow").slideDown();
    $("#participe").slideUp();
  }

  function prepare_to_hide_home_menu() {
    if (home_menu_delay) clearTimeout(home_menu_delay);
    home_menu_delay = setTimeout(function() {
      home_menu_delay = null;
      hide_home_menu();
    }, 500);
  }

  $("#a-participe").hover(show_home_menu, prepare_to_hide_home_menu);

  $("#participe .govresponde, " +
    "#participe .govpergunta, " +
    "#participe .govescuta,   " +
    "#participe .agenda")
        .hover(function() {
            $(this).addClass('selected');
            $("#participe .desc").text($(this).data("text"));
        }, function() {
            $("#participe .desc").text('');
            $(this).removeClass('selected');
        });
});

function goto(url) {
  return function() {
    document.location.href = url;
  };
}