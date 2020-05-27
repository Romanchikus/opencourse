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

function enroll_ask(course) {
  data = {
    course: course
  }
  $.ajax({
    type: "post",
    url: '{% url "courses:enrollment_create" %}',
    data: data,
    // success: function(data) {
    //     $('#cart_count').html(data.cart_total)
    // }
  })
  setInterval(dis_butt, 500);
  $('.enroll_ask').removeAttr('onclick');
  console.log(course)

}

function dis_butt() {
  $('.enroll_ask').prop('disabled', true)
}