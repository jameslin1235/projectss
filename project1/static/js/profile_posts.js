var target = $("#js-target");

$(".js-delete").on("click", function(){
  target.attr("data-url", $(this).attr("data-url"));
  $("#js-delete-modal").toggleClass("hidden");
});

$("#js-delete-post").on("click", function(){
  delete_post().done(function(data){
    window.location.href = window.location.href;
  });
});

function delete_post(){
  var url = target.attr("data-url");
  return $.ajax({
    method: "DELETE",
    url: url
  });
}

$(".js-modal-close").on("click", function(){
  target.removeAttr("data-url");
  $(this).parents(".modal-wrapper").toggleClass("hidden");
});
