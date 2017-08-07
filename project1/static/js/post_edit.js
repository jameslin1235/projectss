$("#js-form").on("submit", function(e){
  e.preventDefault();
  var form = $("#js-form");
  var url = form.attr("data-url");
  var data = form.serialize();
  $.ajax({
  method: "PATCH",
  url: url,
  data: data
})
  .done(function( response ) {
    console.log('w');
  });
});
