// LIKE POST  //
$(".js-post-like").on("click", function() {
  var element = $(this);
  var id = element.parents(".contentitem").attr("data-id");
  var liked = "unliked";
  if (element.hasClass("button--active")) {
    liked = "liked";
  }
  post_like(id,liked).done(function(response){
    element.children().last().text(response["likes"]);
    element.toggleClass("button--active");
  });

  });

function post_like(id,liked){
  var data = {};
  data["id"] = id;
  data["liked"] = liked;
  return $.ajax({
    url: "/posts/like/",
    data: data
  });
}
////
