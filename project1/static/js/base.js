// function make_message(message){
//   var message = '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+message+'</div>';
//   return message;
// }

// a message box will slide down, slide up, and remvoed below navigation bar

function get_notification(message){
  $.ajax({     // ajax GET to get notification
    url: "/getnotification/",
    data:{
      message:message,
    },
    success:function(data) {

      $(".navbar-fixed-top").after(data);
      $(".notification").hide().show(2000).hide(500);
    }});

}



function get_login_modal(){
  $.ajax({     // ajax GET to /getloginmodal/
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

    $(document).on('click', '.Paginationbtn', function() {
      event.preventDefault();
      var element = $(this);
      var url = $(element).attr("data-url");
      var parent = (element).parents(".ContentItem")
      $.ajax({     // ajax GET to get nth page
        url: url,
        success:function(data) {
          $(parent).find(".ContentItem_comments").replaceWith(data);
          $(parent).find(".ContentItem_comments").collapse('show');
        }});
      });


    // Feature 1 Like item
    $(document).on('click', '.like_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var parent = (element).parents(".ContentItem");
      var item_url = $(parent).attr("data-url");
      var user_status = $("#user_status").attr("data-user-status");
      if (user_status == "anonymous") {
        get_login_modal();
      }
      else if (user_status == "user"){
        $.ajax({  // ajax GET to /posts/id/slug/like
          url:item_url + "like",
          success:function(data) {
            if ($(element).hasClass("active")) {
              $(element).removeClass("active");
            }
            else{
              $(element).addClass("active");
            }
            $(parent).find(".ContentItem_likers_count").html(data.likes_count+" people liked this post.");
            $(parent).find(".ContentItem_actions_likers_count").html(data.likes_count);
          }
        });
      }
    });

    // Feature 2 Dislike item
    $(document).on('click', '.dislike_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var parent = (element).parents(".ContentItem");
      var item_url = $(parent).attr("data-url");
      var user_status = $("#user_status").attr("data-user-status");
      if (user_status == "anonymous") {
        get_login_modal();
      }
      else if (user_status == "user"){
        $.ajax({  // ajax GET to /posts/id/slug/dislike
          url:item_url + "dislike",
          success:function(data) {
            if ($(element).hasClass("active")) {
              $(element).removeClass("active");
            }
            else{
              $(element).addClass("active");
            }
            $(parent).find(".ContentItem_actions_dislikers_count").html(data.dislikes_count);
          }
        });
      }
    });

    // Feature 3 post comments collapse
    $(document).on('click', '.comment_button', function(event) {
      event.preventDefault();
      var element = $(this);
      var parent = (element).parents(".ContentItem")
      var item_url = $(parent).attr("data-url");
      if ($(parent).find(".ContentItem_comments").length) {
        var ContentItem_comments = $(parent).find(".ContentItem_comments");
        $(ContentItem_comments).collapse('hide');
        $(ContentItem_comments).on('hidden.bs.collapse', function () {
          $(ContentItem_comments).remove();});
      }
      else{
        $.ajax({  // ajax GET to /posts/id/slug/comments
          url:item_url + "comments",
          success:function(data) {
            $(parent).append(data);
            $(parent).find(".ContentItem_comments").collapse('show');
            autosize($('textarea'));
          }
        });
      }

    });

    // Feature 8 Post comment to DB, show first page of post comments, show message
    $(document).on('submit', '.ContentItem_comments_form', function(event) {
      event.preventDefault();
      var element = $(this);
      var parent = (element).parents(".ContentItem");
      var item_url = $(parent).attr("data-url");
      var method = $(element).attr('method');
      var content = $(parent).find(".ContentItem_comments_form_textfield").val();
      var csrf_token = $(parent).find("[type='hidden']").val();
      $.ajax({  // ajax POST to save comment /posts/id/slug/
        method: method,
        url: item_url,
        data: {
          content: content,
          csrfmiddlewaretoken:csrf_token,
        },
        success:function(data) {
          var message = data.message;
          $.ajax({  // ajax GET to /posts/id/slug/comments
            url:item_url + "comments",
            success:function(data) {
              $(parent).find(".ContentItem_comments").replaceWith(data);
              // gif
              // 
              $(parent).find(".ContentItem_comments").collapse('show').hide();

              $.ajax({
                url:item_url + "commentscount",  // ajax GET to /posts/id/slug/commentscount
                success:function(data){
                  $(parent).find(".ContentItem_actions_comments_count").html(data.post_comments_count);
                  get_notification(message);
                }
              });
            }
          });

          },
        });
      });



          // Feature 6 Open comment form buttons
          $(document).on('click', '.ContentItem_comments_form_textfield', function(event) {
            event.preventDefault();
            var element = $(this);
            var parent = (element).parents(".ContentItem")
            var user_status = $("#user_status").attr("data-user-status");
            if (user_status == "anonymous") {
              get_login_modal();
            }
            else {
              $(parent).find(".ContentItem_comments_form_collapse").collapse('show');
            }
          });

          // Feature 7 Close comment form buttons
          $(document).on('click', '.ContentItem_comments_form_cancel_btn', function(event) {
            event.preventDefault();
            var element = $(this);
            var parent = (element).parents(".ContentItem")
            $(parent).find(".ContentItem_comments_form_collapse").collapse('hide');
          });
