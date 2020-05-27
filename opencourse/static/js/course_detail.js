$("#contact_request").click(function () {
  let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  let url = $("#contact_request").attr("data-ajax-target")
  $.post(url)
})

$("#enroll").click(function() {
  let form = $("#enrollment-form")
  let url = form.attr('action');
  let button = $(this)

  $.post({
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function (data) {
      console.log(data); // show response from the php script.
      $("#enrollment-sent-alert").removeClass("d-none");
      button.hide();
    }
  });
})
