// SHOW DRAFT DELETE MODAL //
$(".js-draft-delete").on("click", function() {
  var url = $(this).parents(".contentitem").attr("data-url");
  console.log(url);
  var template = "draft_delete_modal.html";
  get_modal(template).done(function(modal){
    $("body").append(modal);
    $("#js-draft-delete-link").attr("href",url + "delete/");
    $(".modal__wrapper").animate({top: 0});
  });
  });
////
