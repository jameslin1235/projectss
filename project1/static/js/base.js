function make_message(message){
  var message = '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+message+'</div>';
  return message;
}

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

function get_login_modal(){
  $.ajax({     // ajax GET to get and open login modal
    url: "/getloginmodal/",
    success:function(data) {
      $("body").append(data);
      $("#login_modal").modal();
    }});
  }

  // Feature 1 Close login modal
  $(document).on('click', '#login_modal_close_button', function(event) {
    event.preventDefault();
    $('#login_modal').modal('hide');
  });

  // Feature 2 Remove login modal once it is hidden
  $(document).on('hidden.bs.modal', '#login_modal', function(event) {
    event.preventDefault();
    var element = $(this);
    $(element).remove();
  });


  // Feature 1 Get nth page of paginated results
  $(document).on('click', '.page_button', function() {
    event.preventDefault();
    var element = $(this);
    var url = $(element).attr("href");

    $.ajax({     // ajax GET to get nth page
      url: url,
      success:function(data) {
        $(".list_page").replaceWith(data);
        // $("#profile_posts_select").val(option);
      }});
    });

    // Feature 1 Like item
    $(document).on('click', '.like_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var item_url = $(element).parents(".ContentItem").attr("data-url");
      var user_status = $("#user_status").attr("data-user-status");
      if (user_status == "anonymous") {
        get_login_modal();
      }
      else if (user_status == "user"){
        $.ajax({  // ajax GET to like item
          url:item_url + "like",
          success:function(data) {
            // status = data.status;
            if ($(element).hasClass("active")) {
              $(element).removeClass("active");
            }
            // if (status == "unliked") {
            //   $(element).attr("class","btn btn-primary like_button");
            // }
            else{
              $(element).addClass("active");

              // $(element).attr("class","btn btn-primary like_button active");
            }
            $(element).parents(".ContentItem").find(".ContentItem_likers_count").html(data.likes_count+" people liked this post.");
            $(element).parents(".ContentItem").find(".ContentItem_actions_likers_count").html(data.likes_count);
          }
        });
      }
    });

    // Feature 2 Dislike item
    $(document).on('click', '.dislike_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var item_url = $(element).parents(".ContentItem").attr("data-url");
      var user_status = $("#user_status").attr("data-user-status");
      if (user_status == "anonymous") {
        get_login_modal();
      }
      else if (user_status == "user"){
        $.ajax({  // ajax GET to like item
          url:item_url + "dislike",
          success:function(data) {
            // status = data.status;
            if ($(element).hasClass("active")) {
              $(element).removeClass("active");
            }
            else{
              $(element).addClass("active");
            }
            $(element).parents(".ContentItem").find(".ContentItem_actions_dislikers_count").html(data.dislikes_count);
          }
        });
      }
    });

    // Feature 3 Comments
    $(document).on('click', '.comment_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var item_url = $(element).parents(".ContentItem").attr("data-url");
      if ($(element).parents(".ContentItem").find(".ContentItem_comments").length) {
        var ContentItem_comments = $(element).parents(".ContentItem").find(".ContentItem_comments");
        $(ContentItem_comments).collapse('hide');
        $(ContentItem_comments).on('hidden.bs.collapse', function () {
          $(ContentItem_comments).remove();});
      }
      else{
        $.ajax({  // ajax GET to like item
          url:item_url + "comments",
          success:function(data) {
            $(element).parents(".ContentItem").append(data);
            $(element).parents(".ContentItem").find(".ContentItem_comments").collapse('open');
          }
        });
      }

    });
