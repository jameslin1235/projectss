var target = $("#js-target");

$(".js-delete").on("click", function(){
  var url = $(this).attr("data-url");
  target.attr("data-url", url);
  $("#js-delete-modal").toggleClass("hidden");
});

$("#js-delete-draft").on("click", function(){
  delete_draft().done(function(data){
    window.location.href = window.location.href;
  });
});

$(".js-publish").on("click", function(){
  target.attr("data-url", $(this).attr("data-url"));
  $("#js-publish-modal").toggleClass("hidden");
});

$("#js-publish-draft").on("click", function(){
  publish_draft().done(function(data){
    window.location.href = data["url"];
  });
});

function delete_draft(){
  var url = target.attr("data-url");
  return $.ajax({
    method: "DELETE",
    url: url
  });
}

function publish_draft(){
  var url = target.attr("data-url");
  var data = {publish:""};
  return $.ajax({
    method: "PATCH",
    url: url,
    data: data
  });
}

$(".js-modal-close").on("click", function(){
  target.removeAttr("data-url");
  $(this).parents(".modal-wrapper").toggleClass("hidden");
});
