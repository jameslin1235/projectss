function get_notification(callback, args){
  var message = args[0];
  $.ajax({     // ajax GET to /getnotification/
    url: "/getnotification/",
    data:{
      message:message,
    },
    success:function(data) {
      var callback_args = [data];
      callback(callback_args);
      }});
}

function add_notification(args){
  console.log("add_notification");
  var data = args[0];
  $("body").append(data);
  $(".notification").hide().slideDown(500).delay(3000).slideUp(500,function(){$(this).remove();});
}

function get_login_modal(){
      $.ajax({     // ajax GET to /getloginmodal/
        url: "/getloginmodal/",
        success:function(data) {
          $("body").append(data);
          $("#login-modal").modal();
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

function get_user_status(){
  var user_status = $("#user-status").attr("data-user-status");
  return user_status;
}

// function get_loader(callback, callback_args){
//   $.ajax({      // ajax GET to /getloader/
//     url: "/getloader/",
//     success:function(data) {
//       callback_args.push(data);
//       callback(callback_args);
//       get_post_comments();
//     }});
//   }
//
function get_loader(){
  return $.ajax({      // ajax GET to /getloader/
    url: "/getloader/",
  });
}

function save_comment(args){
  var method = args[0];
  var item_url = args[1];
  var data = args[2];
  return $.ajax({
    method: method,
    url: item_url,
    data: data,
  });
}

function get_post_comments(args){
  var item_url = args[0];
  var template = args[1];
  return $.ajax({  // ajax GET to /posts/id/slug/comments using template
    url:item_url + "comments",
    data: {
      template:template,
    }
});}

function get_post_comments_count(args){
  var item_url = args[0];
  return $.ajax({
    url:item_url + "commentscount",  // ajax GET to /posts/id/slug/commentscount

  });
}

function post_comments_collapse(callbacks,callback_args,args){
  var callback1 = callbacks[0];
  var callback2 = callbacks[1];
  var callback1_args = callback_args[0];
  var callback2_args = callback_args[1];
  console.log(callback1_args);
  var parent = args[0];
  var template = args[1];
  var loader = args[2];
  var comments = args[3];


  if (template == "template2") {
    $(parent).find(".ContentItem-comments-body").remove();
    $('body').animate({scrollTop: $(parent).find(".ContentItem-time").offset().top}, 0, function(){$(parent).find(".ContentItem-comments-topbar").after(loader);});
  }
  else if (template == "template3"){
    $(parent).find(".ContentItem-comments-container").remove();
    $('body').animate({scrollTop: $(parent).find(".ContentItem-time").offset().top}, 0, function(){
      console.log('s');
      $(parent).find(".ContentItem-comments").append(loader);
      $(parent).find(".loader").fadeOut(1000,function(){
        $(this).replaceWith(comments);
        callback1(callback1_args);
        // callback2(callback2_args);

      });
      });
      console.log('sss');

  }
}

// function fade_loader(args){
//   console.log("loader_faded");
//   var parent = args[0];
//   var data = args[1];
//   $(parent).find(".loader").fadeOut(1000,function(){$(this).replaceWith(data);});
// }

function update_post_comments_count(args){
  var parent = args[0];
  var data = args[1];
  console.log(data);
  console.log("update_p_c_count");
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
    var data = {content:content, csrfmiddlewaretoken:csrf_token};

    $.when(get_loader(),save_comment([method, item_url, data]),get_post_comments([item_url, template]),get_post_comments_count([item_url])).done(function(a1, a2, a3, a4){
      var loader = a1[0];
      var message = a2[0];
      var comments = a3[0];
      var comments_count = a4[0];

      var callbacks = [update_post_comments_count,get_notification];
      var callback_args = [[parent,comments_count],[add_notification,message]];
      var args = [parent,template,loader,comments];
      post_comments_collapse(callbacks,callback_args,args);
      // update_post_comments_count([parent,comments_count]);
      // get_notification(add_notification,[message]);
      // console.log(a1);
      // console.log(a2);
      // console.log(a3);
      // console.log(a4);

    });
    // $.ajax({  // ajax POST to save comment /posts/id/slug/
    //   method: method,
    //   url: item_url,
    //   beforeSend:function(){
    //     get_loader(post_comments_collapse,[parent,template]); // ajax GET to /getloader/
    //   },
    //   data: {
    //     content: content,
    //     csrfmiddlewaretoken:csrf_token,
    //   },
    //   success:function(data) {
    //     console.log("post_saved");
    //     var message = data.message;
    //     get_post_comments(fade_loader,[parent],[item_url,template]); // ajax GET to /posts/id/slug/comments using template
    //     console.log("comments_grabbed");
    //     get_post_comments_count(update_post_comments_count,[parent],[item_url]); // ajax GET to /posts/id/slug/commentscount
    //     get_notification(add_notification,[message]); // ajax GET to /getnotification/
    //
    // }});
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
