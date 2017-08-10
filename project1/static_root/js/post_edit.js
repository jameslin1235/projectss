$("#js-form").on("submit", function(e){
  e.preventDefault();
  var form = $(this);
  var url = form.attr("data-url");
  var data = form.serialize();
  $.ajax({
    method: "PATCH",
    url: url,
    data: data
  }).done(function( response ) {
    window.location.href = response["url"];
  });
});
