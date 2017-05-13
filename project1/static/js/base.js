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
      $("body").append(data);
      $(".notification").hide().slideDown(500).delay(3000).slideUp(500,
        function(){$(this).remove();});

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


      function get_loader(parent,template){
        $.ajax({     // ajax GET to get loader
          url: "/getloader/",
          success:function(data) {
            if (template == "template2") {
              $(parent).find(".ContentItem_comments_body").remove();
              $('body').animate({
                scrollTop: $(parent).find(".ContentItem_time").offset().top
              }, 0);
              $(parent).find(".ContentItem_comments_topbar").after(data);
            }
            else if (template == "template3"){
              $(parent).find(".ContentItem_comments_container").remove();
              $('body').animate({
                scrollTop: $(parent).find(".ContentItem_time").offset().top
              }, 0);
              $(parent).find(".ContentItem_comments").append(data);
            }

          }});
        }

        $(document).on('click', '.btn-pagination', function() {
          event.preventDefault();
          var element = $(this);
          var url = $(element).attr("data-url");
          var parent = (element).parents(".ContentItem");
          var template2 = "template2";
          $.ajax({     // ajax GET to /posts/id/slug/comments/?page=
            url: url,
            beforeSend:get_loader(parent,template2),
            data: {
              template2:template2,
            },
            success:function(data) {
              $(parent).find(".loader").fadeOut(1000,
                function(){$(parent).find("#loader").replaceWith(data);
              });
            }});
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
            var template3 = "template3";
            $.ajax({  // ajax POST to save comment /posts/id/slug/
              method: method,
              url: item_url,
              beforeSend:get_loader(parent,template3),
              data: {
                content: content,
                csrfmiddlewaretoken:csrf_token,
              },
              success:function(data) {
                var message = data.message;
                $.ajax({  // ajax GET to /posts/id/slug/comments using template 3
                  url:item_url + "comments",
                  data: {
                    template3:template3,
                  },
                  success:function(data) {
                    $(parent).find(".loader").fadeOut(1000,
                      function(){
                        $(parent).find("#loader").replaceWith(data);
                        $.ajax({
                          url:item_url + "commentscount",  // ajax GET to /posts/id/slug/commentscount
                          success:function(data){
                            $(parent).find(".ContentItem_actions_comments_count").html(data.post_comments_count);
                            get_notification(message);
                          }
                        });
                      });
                    }
                  });
                },
              });
            });

            //
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
                  $.ajax({  // ajax GET to /posts/id/slug/comments (brand new collapse)
                    url:item_url + "comments",
                    success:function(data) {
                      $(parent).append(data);
                      $(parent).find(".ContentItem_comments").collapse('show');
                      autosize($('textarea'));
                    }
                  });
                }

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
                var parent = $(element).parents(".ContentItem");
                $(parent).find(".ContentItem_comments_form_collapse").collapse('hide');





              });


              // Feature 3 Get and open post likers modal
              $(document).on('click', '.btn-ContentItem_likers_count', function(event) {
                event.preventDefault();
                var element = $(this);
                var parent = $(element).parents(".ContentItem");
                var item_url = $(parent).attr("data-url");
                $.ajax({     // ajax GET to /posts/id/slug/likers
                  url: item_url + "likers",
                  success:function(data) {
                    $("body").append(data);
                    $(".modal").modal();
                  }});
                });

                // Feature 4 Close post likers modal
                $(document).on('click', '.btn-closeModal', function(event) {
                  event.preventDefault();
                  var element = $(this);
                  var parent = $(element).parents(".modal");
                  $(parent).modal('hide');
                });

                // Feature 5 Remove post likers modal once it is hidden
                $(document).on('hidden.bs.modal', '.modal', function(event) {
                  event.preventDefault();
                  var element = $(this);
                  $(element).remove();
                });

                // Feature 6 Get more post likers
                $(document).on('click', '#post_likers_more_button', function() {
                  event.preventDefault();
                  var element = $(this);
                  var url = $(".post_container").attr("data-url");
                  var nextpage = $("#post_likers_more_container").attr("data-nextpage");

                  $.ajax({     // ajax GET to get next page of post likers
                    url: url + "likers/?page=" + nextpage,
                    success:function(data) {
                      $("#post_likers_more_container").remove();
                      $("#post_likers_modal_body").append(data);
                    }});
                  });

                  // Feature 7 Post likers modal follow buttons
                  $(document).on('click','.post_likers_modal_follow_button',function(){
                    event.preventDefault();
                    var element = $(this);
                    var url= $(element).parents(".post_likers_modal_profile_container").attr("data-url");
                    if ($("#logged_in").data("logged-in")== true) {
                      $.ajax({
                        url: url + "follow",  // ajax GET to follow/unfollow a profile
                        success:function(data) {
                          $(element).html(data.message);
                          $.ajax({  // ajax GET to get profile followers count
                            url: url + "followerscount",
                            success:function(data) {
                              $(element).parents(".post_likers_modal_profile_container").find(".post_likers_modal_followers_count").html(data.profile_followers_count + " Followers");
                            }});
                          }});
                        }
                        else{
                          get_login_modal();
                        }
                      });

                      // Feature 8 Post likers modal follow buttons mouseenter effect
                      $(document).on('mouseenter','.post_likers_modal_follow_button',function(){
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

                      // Feature 9 Post likers modal follow buttons mouseleave effect
                      $(document).on('mouseleave','.post_likers_modal_follow_button',function(){
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
