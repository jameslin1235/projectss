
// Feature 1 user_follow_button
$(document).on('click','.user_follow_button',function(){
  event.preventDefault();
  var element = $(this);
  var user_profile_url= $(element).parents("#profile_base").attr("data-user-profile-url");
  var user_status = $("#user_status").attr("data-user-status");
  if (user_status == "anonymous") {
    get_login_modal();
  }
  else if (user_status == "user"){
    $.ajax({ // ajax GET to follow/unfollow user profile
      url: user_profile_url + "follow",
      success:function(data) {
        $(element).html(data.message);
        $.ajax({  // ajax GET to get user profile followers count
          url: user_profile_url + "followerscount",
          success:function(data) {
            $(element).parents("#profile_base").find(".profile_sidebar_followers_count").html(data.profile_followers_count);
            var profile_followers_page = $(element).parents("#profile_base").find("#profile_followers_page")
            if (profile_followers_page.length){
              $(element).parents("#profile_base").find(".list_page_header").html(data.profile_followers_count);
            }
          }});
        }});
      }

    });

    // Feature 2 user_follow_button mouseenter effect
    $(document).on('mouseenter','.user_follow_button, .list_item_follow_button',function(){
      event.preventDefault();
      var element = $(this);
      if ($("#logged_in").data("logged-in")== true){
        if ($(element).html() == "Followed") {
          $(element).html("Unfollow");
        }
      }
      else{
        event.preventDefault();
      }
    });

    // Feature 3 user_follow_button mouseleave effect
    $(document).on('mouseleave','.user_follow_button, .list_item_follow_button',function(){
      event.preventDefault();
      var element = $(this);
      if ($("#logged_in").data("logged-in")== true){
        if ($(element).html() == "Unfollow") {
          $(element).html("Followed");
        }
      }
      else{
        event.preventDefault();
      }
    });