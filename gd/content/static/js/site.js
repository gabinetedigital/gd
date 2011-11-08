$(function () {

  $("#govresponde").data('text','Quer saber o que o governador pensa? Pergunte para ele. A questão mais votada do mês é respondida em vídeo.');
  $("#govpergunta").data('text', 'O Governador pergunta e a sociedade responde com novas idéias.');
  $("#agenda").data('text', 'Quer fazer parte da agenda do governador na sua cidade? Indique uma pauta na agenda colaborativa.');
  $("#govescuta").data('text','Audiências públicas digitais transmitidas via internet onde você pode enviar sua contribuição.');

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

  $("#govresponde, #govpergunta, #govescuta, #agenda").hover(function() {
    var self = $(this);
    $("#desc").text(self.data("text"));
    var bg = self.css("background-image");
    self.css("background-image",bg.replace("base","selected"));
  }, function() {
    $("#desc").text('');
    var self = $(this);
    var bg = self.css("background-image");
    self.css("background-image",bg.replace("selected","base"));
  });
});

function goto(url) {
  return function() {
    document.location.href = url;
  }
}