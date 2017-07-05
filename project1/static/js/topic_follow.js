$(".js-topic-follow").on("click", function() {
    var id = $(this).attr("id");
    $("#item-icon-" + id).toggleClass("fa-check");
  });

$("#js-topic-submit").on("click", function(){
  var id = [];
  $(".js-item-icon").each(function(){
    if ($(this).hasClass("fa-check")) {
      id.push(Number($(this).attr("id").replace("item-icon-", "")));
    }
  });
  var url = "http://localhost:8000/topics/follow/?id=" + id;
  window.location.replace(url);
});
