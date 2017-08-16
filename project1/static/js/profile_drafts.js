$(".js-delete").on("click", function(){
  var url = $(this).parents(".post").attr("data-url");
  $("#js-delete-draft").attr("data-url", url);
  $("#js-delete-modal").toggleClass("hidden");
});

$(".js-delete-modal-close").on("click", function(){
  $("#js-delete-draft").removeAttr("data-url");
  $("#js-delete-modal").toggleClass("hidden");
});

$("#js-delete-draft").on("click", function(){
  var url = $(this).attr("data-url");
  $.ajax({
    method: "DELETE",
    url: url
  }).done(function( response ) {
    window.location.href = response["url"];
  });
});

$(".js-publish").on("click", function(){
  var url = $(this).parents(".post").attr("data-url");
  $("#js-publish-draft").attr("data-url", url);
  $("#js-publish-modal").toggleClass("hidden");
});

$(".js-publish-modal-close").on("click", function(){
  $("#js-publish-draft").removeAttr("data-url");
  $("#js-publish-modal").toggleClass("hidden");
});

$("#js-publish-draft").on("click", function(){
  var url = $(this).attr("data-url");
  var data = {publish:""};
  $.ajax({
    method: "PATCH",
    url: url,
    data: data
  }).done(function( response ) {
    window.location.href = response["url"];
  });
});
