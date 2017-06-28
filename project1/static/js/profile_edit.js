// EDIT PROFILE BACKGROUND //
$(".js-profile-background-edit").on("click", function() {
  $(".js-profile-background-field").click();
});
////

// EDIT PROFILE AVATAR //
$(".js-profile-avatar-edit").on("click", function(event) {
  $("#id_avatar").click();
});

$("#id_avatar").on("click", function(event) {
  event.stopPropagation();
});

////
