// SHOW POST DELETE MODAL //
$(".js-post-delete").on("click", function() {
  var url = $(this).parents(".contentitem").attr("data-url");
  var template = "post_delete_modal.html";
  get_modal(template).done(function(modal){
    $("body").append(modal);
    $("#js-post-delete-link").attr("href", url + "delete/");
    $(".modal__wrapper").animate({top: 0});
  });
  });
////
