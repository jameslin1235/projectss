// SHOW DRAFT DELETE MODAL //
$(".js-draft-delete").on("click", function() {
  var url = $(this).parents(".contentitem").attr("data-url");
  var template = "draft_delete_modal.html";
  get_modal(template).done(function(modal){
    $("body").append(modal);
    $("#js-draft-delete-link").attr("href", url + "delete/");
    $(".modal__wrapper").animate({top: 0});
  });
  });
////

// SHOW DRAFT PUBLISH MODAL //
$(".js-draft-publish").on("click", function() {
  var url = $(this).parents(".contentitem").attr("data-url");
  var template = "draft_publish_modal.html";
  get_modal(template).done(function(modal){
    $("body").append(modal);
    $("#js-draft-publish-link").attr("href", url + "publish/");
    $(".modal__wrapper").animate({top: 0});
  });
  });
////
