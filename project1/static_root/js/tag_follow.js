// Toggle between selecting/unselecting tag
$(".js-tag").on("click", function(){
  $(this).children(".js-layer").toggleClass("hidden");
});

// Check for selected tags and build relationships (user follows tags)
$("#js-follow-tags").on("click", function(){
  var id = [];
  var url = "/tags/follow/";
  $(".js-tag").each(function(){
    if (!$(this).children(".js-layer").hasClass("hidden")) {
      id.push(Number($(this).attr("data-id")));
    }
  });
  if (id.length === 0) {
    window.location.href = url;
  }
  else{
    window.location.href = url + "?id=" + id;
  }
});
