
// $(".js-post-create-form").on("submit", function(event) {
//   event.preventDefault();
//   var element = $(this);
//   var data = element.serialize();
//   submit_post(data).done(function(response){
//     var message = "Post created.";
//     get_alert(message).done(function(alert){
//       $("body").animate({scrollTop:0}, function(){add_alert(alert);});
//     });
//   });
// });
//
// function submit_post(data){
//   return $.ajax({
//     url: "/posts/create/",
//     data: data,
//     method: "POST"
//   });
// }
////
