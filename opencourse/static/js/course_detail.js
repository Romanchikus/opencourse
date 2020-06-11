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

window.onload = function loadContIcons() {
  var count_value = document.getElementById("ReviewCountCl").getAttribute('value');
  var newspan = document.createElement("span");
  newspan.setAttribute("style", 'font-size: large');
  newspan.innerHTML = count_value.toString();
  var divsParent = document.getElementsByClassName("rating-container")[0];
  divsParent.appendChild(newspan);
  console.log(newspan);
};