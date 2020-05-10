$(function () {
  $('.selectmultiple').selectpicker({noneSelectedText: '---------'});
  $('.bootstrap-select button').addClass("form-control")

  options = {
    min: 0,
    max: 5,
    step: 1,
    size: 'sm',
    showClear: false,
    showCaption: false,
    theme: 'krajee-uni',
  }
  $("#id_score").rating(options);

  options.displayOnly = true
  $(".score-display").rating(options);

  $('.change-language').click(function (e) {
    $('#language').val($(this).attr('data-lang-code'));
    $('#change-language-form').submit();
  });
});
