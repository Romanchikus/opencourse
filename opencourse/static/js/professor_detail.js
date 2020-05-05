$(function () {
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

  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
});

function contact_request() {
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  var url = $("#contact_request").attr("data-ajax-target")
  $.post(url)
  console.log(url)
};
