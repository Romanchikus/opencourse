  $('.status-togle').click(function (e) {
    let url = $(this).attr('data-ajax-target');
    let status = $(this).attr('data-status');
    let data = {status: status}
    let button_to_enable = $(this).parent().find(`button[data-status!=${status}]`)
    let button_to_disable = $(this).parent().find(`button[data-status=${status}]`)

    $.post(url, data, function (button=this) {
      button_to_disable.addClass("disabled");
      button_to_enable.removeClass("disabled")

    })
  });


function enroll_ask(course) {
  data = {
    course: course
  }
  $.ajax({
    type: "post",
    url: '{% url "handouts:post" %}',
    data: data,
  })
  setInterval(dis_butt, 500);
  $('.enroll_ask').removeAttr('onclick');
  console.log(course)

}

function dis_butt() {
  $('.enroll_ask').prop('disabled', true)
}

$(document).ready(function () {
  $('.add_enrollment').on("click", function (e) {
    e.preventDefault()
    let action = $(this).attr('data-bool')
    let id_button = $(this).attr('id')
    let enrol_slug = $(this).attr('data-slug')
    let course_slug = $(this).attr('course_slug')

    let data = {
      enrol_slug: enrol_slug,
      action: action,
      course_slug: course_slug
    }
    a = document.getElementsByClassName(id_button)
    let len = a.length;
    for (let i = 0; i < len; i++) {
      a[i].disabled = true;
      console.log(a[i]);
    }
    document.getElementById(id_button).disabled = true;
    console.log('#li_'.concat(id_button))
    $.ajax({
      type: "put",
      url: '{% url "handouts:post" %}',
      data: data,
      success: function (data) {

      }
    })
  })
})
