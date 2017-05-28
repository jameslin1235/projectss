//
// // Feature 1 user_follow_button
// $(document).on('click','.user_follow_button',function(){
//   event.preventDefault();
//   var element = $(this);
//   var user_profile_url= $(element).parents("#profile_base").attr("data-user-profile-url");
//   var user_status = $("#user_status").attr("data-user-status");
//   if (user_status == "anonymous") {
//     get_login_modal();
//   }
//   else if (user_status == "user"){
//     $.ajax({ // ajax GET to follow/unfollow user profile
//       url: user_profile_url + "follow",
//       success:function(data) {
//         $(element).html(data.message);
//         $.ajax({  // ajax GET to get user profile followers count
//           url: user_profile_url + "followerscount",
//           success:function(data) {
//             $(element).parents("#profile_base").find(".profile_sidebar_followers_count").html(data.profile_followers_count);
//             var profile_followers_page = $(element).parents("#profile_base").find("#profile_followers_page")
//             if (profile_followers_page.length){
//               $(element).parents("#profile_base").find(".list_page_header").html(data.profile_followers_count);
//             }
//           }});
//         }});
//       }
//
//     });
//
//     // Feature 2 user_follow_button mouseenter effect
//     $(document).on('mouseenter','.user_follow_button, .list_item_follow_button',function(){
//       event.preventDefault();
//       var element = $(this);
//       if ($("#logged_in").data("logged-in")== true){
//         if ($(element).html() == "Followed") {
//           $(element).html("Unfollow");
//         }
//       }
//       else{
//         event.preventDefault();
//       }
//     });
//
//     // Feature 3 user_follow_button mouseleave effect
//     $(document).on('mouseleave','.user_follow_button, .list_item_follow_button',function(){
//       event.preventDefault();
//       var element = $(this);
//       if ($("#logged_in").data("logged-in")== true){
//         if ($(element).html() == "Unfollow") {
//           $(element).html("Followed");
//         }
//       }
//       else{
//         event.preventDefault();
//       }
//     });

// pagination for list_page in profile section

$(document).on('click', '.btn-pagination', function() {
  event.preventDefault();
  var element = $(this);
  if ($(element).parent(".ContentItem-Pagination").length){
    var parent = (element).parents(".ContentItem");
    var item_comments_url = $(element).attr("data-url");
    var template = "template2";
    var args = [item_comments_url, template];
    $.when(get_loader(),get_item_comments_page(args)).done(function(a1, a2){
      var loader = a1[0];
      var item_comments = a2[0];
      var args = [parent,loader,item_comments];
      add_item_comments_page(args);
    });
  }
  else{
    var parent = (element).parents(".List");
    var list_page_url = $(element).attr("data-url");
    var args = [list_page_url]
    $.when(get_loader(),get_list_page(args)).done(function(a1, a2){
      var loader = a1[0];
      var list_page = a2[0];
      var args = [parent,loader,list_page];
      add_list_page(args);
    });
  }
});


// Get & Add profile form
function get_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  edit_profile_url = args[0]
  return $.ajax({
    url: edit_profile_url,
  });
}

function add_profile_form(){
    var args = Array.prototype.slice.call(arguments);
    parent = args[0];
    profile_form = args[1];
    $(parent).empty().append(profile_form);
}

// Get & Add profile header, body
function get_profile_header(){
  var args = Array.prototype.slice.call(arguments);
  profile_url = args[0]
  query_string = args[1]
  return $.ajax({
    url: profile_url,
    data: query_string,
  });
}

function get_profile_body(){
  var args = Array.prototype.slice.call(arguments);
  profile_url = args[0]
  query_string = args[1]
  return $.ajax({
    url: profile_url,
    data: query_string,
  });
}

function add_profile(){
    var args = Array.prototype.slice.call(arguments);
    parent = args[0];
    profile_header = args[1];
    profile_body = args[2];
    $(parent).empty().append(profile_header).append(profile_body);
}

$(document).on('click', '.js-edit-profile', function() {
  event.preventDefault();
  var element = $(this);
  var edit_profile_url = $(element).attr("data-url");
  var parent = (element).parents(".profile");
  $.when(get_profile_form(edit_profile_url)).done(function(a1){
    var profile_form = a1;
    add_profile_form(parent,profile_form);
  });

});

$(document).on('click', '.js-get-profile', function() {
  event.preventDefault();
  var element = $(this);
  var profile_url = $(element).attr("data-url");
  var parent = (element).parents(".profile");
  var query_string1 = "profile_header";
  var query_string2 = "profile_body";
  $.when(get_profile_header(profile_url,query_string1),get_profile_body(profile_url,query_string2)).done(function(a1,a2){
    var profile_header = a1[0];
    var profile_body = a2[0];
    add_profile(parent,profile_header,profile_body);
  });
});
