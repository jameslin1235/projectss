function get_notification(callback, callback_args = ["default"], args){
  console.log(callback_args);
  console.log(args);
  var message = args[0];
  $.ajax({     // ajax GET to get notification
    url: "/getnotification/",
    data:{
      message:message,
    },
    success:function(data) {
      callback_args[0] = (data);
      callback(callback_args);
      }});
}

function add_notification(args){
  var message = args[0];
  $("body").append(message);
  $(".notification").hide().slideDown(500).delay(3000).slideUp(500,
          function(){$(this).remove();});
}
function get_login_modal(){
      $.ajax({     // ajax GET to /getloginmodal/
        url: "/getloginmodal/",
        success:function(data) {
          $("body").append(data);
          $("#login-modal").modal();
        }});
}

function get_user_status(){
  var user_status = $("#user-status").attr("data-user-status");
  return user_status;
}

function get_ajax_data(data){
  post_comments_collapse(data);
  console.log(data);

}

// var func = arguments[0];
// var args = Array.prototype.slice.call(arguments, 1)
// console.log(func);
// args.push(data);
// func(args);
function get_loader(callback, args){
  // console.log(arguments);
  //
  // for (var i = 0; i < arguments.length; i++) {
  //     console.log(arguments[i]);
  //   }
  $.ajax({     // ajax GET to /getloader/
    url: "/getloader/",
    success:function(data) {
      args.push(data);
      // console.log(arguments);
      // console.log(args);
      // console.log(args[0]);
      // console.log(args[1]);
      // console.log(args[2]);
      callback(args);
      // callback.apply(this,args);
    }});
  }




// Feature 1 Close login modal
$(document).on('click', '#login-modal-close-button', function(event) {
  event.preventDefault();
  $('#login-modal').modal('hide');
});

// Feature 2 Remove login modal once it is hidden
$(document).on('hidden.bs.modal', '#login-modal', function(event) {
  event.preventDefault();
  var element = $(this);
  $(element).remove();
});



function post_comments_collapse(args){
  var parent = args[0];
  var template = args[1];
  var data = args[2];
  // console.log(args[0]);
  // console.log(args[1]);
  // console.log(args[2]);
  if (template == "template2") {
    $(parent).find(".ContentItem-comments-body").remove();
    $('body').animate({
      scrollTop: $(parent).find(".ContentItem-time").offset().top
    }, 0);
    $(parent).find(".ContentItem-comments-topbar").after(data);
  }
  else if (template == "template3"){
    $(parent).find(".ContentItem-comments-container").remove();
    $('body').animate({
      scrollTop: $(parent).find(".ContentItem-time").offset().top
    }, 0);
    $(parent).find(".ContentItem-comments").append(data);
  }
}

function get_post_comments(callback, callback_args, args){
  var item_url = args[0];
  var template = args[1];
  $.ajax({  // ajax GET to /posts/id/slug/comments using template
    url:item_url + "comments",
    data: {
      template:template,
    },
    success:function(data){
      callback_args.push(data);
      callback(callback_args);
    }
});}

function fade_loader(args){
  var parent = args[0];
  var data = args[1];
  $(parent).find(".loader").fadeOut(1000,function(){
      $(this).replaceWith(data);
  })
}

function get_post_comments_count(callback, callback_args, args){
  var item_url = args[0];
  $.ajax({
    url:item_url + "commentscount",  // ajax GET to /posts/id/slug/commentscount
    success:function(data){
      callback_args.push(data);
      callback(data);
    }
  });
}

function update_comments_count(args){
  var parent = args[0];
  var data = args[1];
  $(parent).find(".ContentItem-actions-comments-count").html(data);

}

$(document).on('click', '.btn-pagination', function() {
  event.preventDefault();
  var element = $(this);
  var url = $(element).attr("data-url");
  var parent = (element).parents(".ContentItem");
  var template2 = "template2";
  $.ajax({     // ajax GET to /posts/id/slug/comments/?page=
    url: url,
    beforeSend:function(){
      var loader = get_loader();
      console.log(loader);
      post_comments_collapse(parent,template2,loader);
    },
    data: {
      template2:template2,
    },
    success:function(data) {
      alert('yes');
      $(parent).find(".loader").fadeOut(1000,
        function(){$(parent).find("#loader").replaceWith(data);
      });
    }});
  });


  // Save comment,
  $(document).on('submit', '.ContentItem-comments-form', function(event) {
    event.preventDefault();
    var element = $(this);
    var parent = (element).parents(".ContentItem");
    var item_url = $(parent).attr("data-url");
    var method = $(element).attr('method');
    var content = $(parent).find(".ContentItem-comments-form-textfield").val();
    var csrf_token = $(parent).find("[type='hidden']").val();
    var template = "template3";

    $.ajax({  // ajax POST to save comment /posts/id/slug/
      method: method,
      url: item_url,
      beforeSend:function(){
        get_loader(post_comments_collapse,[parent,template]);
      },
      data: {
        content: content,
        csrfmiddlewaretoken:csrf_token,
      },
      success:function(data) {
        // var message = data.message;
        // get_post_comments(fadeout,[parent],[item_url,template]);
        // get_post_comments_count(update_comments_count,[item_url])
        // get_notification(add_notification,[message])
        // $(parent).find(".loader").fadeOut(1000,function(){
        //   $(this).replaceWith(post_comments);
        //   var post_comments_count = get_post_comments_count(item_url, get_ajax_data);
        //   $(parent).find(".ContentItem-actions-comments-count").html(post_comments_count);
        //   var message = get_notification(message,get_ajax_data);
        //   $("body").append(message);
        //   $(".notification").hide().slideDown(500).delay(3000).slideUp(500,
        //     function(){$(this).remove();});
      }});
    });


            //
            // Feature 1 Like item
            $(document).on('click', '.like-button', function(event) {
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
                    $(parent).find(".ContentItem-likers-count").html(data.likes_count+" people liked this post.");
                    $(parent).find(".ContentItem-actions-likers-count").html(data.likes_count);
                  }
                });
              }
            });

            // Feature 2 Dislike item
            $(document).on('click', '.dislike-button', function(event) {
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
                    $(parent).find(".ContentItem-actions-dislikers-count").html(data.dislikes_count);
                  }
                });
              }
            });

            // Feature 3 post comments collapse
            $(document).on('click', '.comment-button', function(event) {
              event.preventDefault();
              var element = $(this);
              var parent = (element).parents(".ContentItem")
              var item_url = $(parent).attr("data-url");
              if ($(parent).find(".ContentItem-comments").length) {
                var ContentItem_comments = $(parent).find(".ContentItem-comments");
                $(ContentItem_comments).collapse('hide');
                $(ContentItem_comments).on('hidden.bs.collapse', function () {
                  $(ContentItem_comments).remove();});
                }
                else{
                  $.ajax({  // ajax GET to /posts/id/slug/comments (brand new collapse)
                    url:item_url + "comments",
                    success:function(data) {
                      $(parent).append(data);
                      $(parent).find(".ContentItem-comments").collapse('show');
                      autosize($('textarea'));
                    }
                  });
                }

              });




              // Feature 6 Open comment form buttons
              $(document).on('click', '.ContentItem-comments-form-textfield', function(event) {
                event.preventDefault();
                var element = $(this);
                var parent = (element).parents(".ContentItem")
                var user_status = $("#user_status").attr("data-user-status");
                if (user_status == "anonymous") {
                  get_login_modal();
                }
                else {
                  $(parent).find(".ContentItem-comments-form-collapse").collapse('show');
                }
              });

              // Feature 7 Close comment form buttons
              $(document).on('click', '.ContentItem-comments-form-cancel-btn', function(event) {
                event.preventDefault();
                var element = $(this);
                var parent = $(element).parents(".ContentItem");
                $(parent).find(".ContentItem-comments-form-collapse").collapse('hide');





              });


              // Feature 3 Get and open post likers modal
              $(document).on('click', '.btn-ContentItem-likers-count', function(event) {
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
$(document).on('click', '.btn-more', function() {
event.preventDefault();
var element = $(this);
var parent = $(element).parents(".modal");
var item_url = $(parent).attr("data-url");
var nextpage = $(parent).attr("data-nextpage");

$.ajax({     // ajax GET to /posts/id/slug/likers?page=2
url: item_url + "likers/?page=" + nextpage,
beforeSend:get_loader(parent),
success:function(data) {
$("#post_likers_more_container").remove();
$("#post_likers_modal_body").append(data);
}});
});

// Feature 7 Post likers modal follow buttons
$(document).on('click','.follow-button',function(){
event.preventDefault();
var element = $(this);
var parent = (element).parents(".ContentItem");
var item_url = $(parent).attr("data-url");
var ContentItem_modal_follow_status = $(parent).find(".ContentItem-modal-follow-status");
var ContentItem_modal_meta_StatusItem = $(parent).find(".ContentItem-modal-meta-StatusItem:last-child");
var follow_status = $(ContentItem_modal_follow_status).html();
var user_status = get_user_status();
if (user_status == "anonymous") {
  get_login_modal();
}
else {
  $.ajax({  // ajax GET to /profile/id/slug/follow
    url:item_url + "follow",
    data:{
      follow_status:follow_status,
    },
    success:function(data) {
      $(ContentItem_modal_follow_status).html(data.follow_status);
      $.ajax({
        url:item_url + "followerscount",  // ajax GET to /profile/id/slug/followerscount
        success:function(data){
          $(ContentItem_modal_meta_StatusItem).html(data.profile_followers_count+" Followers");
        }
      });
    }
  });
}
});

// Feature mouseenter follow button
$(document).on('mouseenter','.follow-button',function(){
event.preventDefault();
var element = $(this);
var ContentItem_modal_follow_status = $(element).find(".ContentItem-modal-follow-status");
var user_status = get_user_status();
if (user_status == "anonymous") {
  event.preventDefault();
}
else{
  if ($(ContentItem_modal_follow_status).text() == "Followed") {
    $( ContentItem_modal_follow_status).text("Unfollow");
  }
}
});

// mouseleave follow button
$(document).on('mouseleave','.follow-button',function(){
event.preventDefault();
var element = $(this);
var ContentItem_modal_follow_status = $(element).find(".ContentItem-modal-follow-status");
var user_status = get_user_status();
if (user_status == "anonymous") {
  event.preventDefault();
}
else{
  if ($(ContentItem_modal_follow_status).text() == "Unfollow") {
    $( ContentItem_modal_follow_status).text("Followed");
  }
}
});
