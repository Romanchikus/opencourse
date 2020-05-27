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
}

function enrollment_request() {
  var form = $("#enrollment-form")
  var url = form.attr('action');

  $.post({
    url: url,
    data: form.serialize(), // serializes the form's elements.
    success: function (data) {
      console.log(data); // show response from the php script.
    }
  });
}