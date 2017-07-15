// Sign in / Sign up modal //
$("#js-get-login-modal").on("click",function(){
  get_login_modal().done(function(modal){
    $("body").append(modal);
    });
});

function get_login_modal(){
  return $.ajax({
    url: "/getloginmodal/"
  });
}

// Sign in / Sign up modal tab toggle //
$(document).on("click", "#js-login-tab-toggle", function(){
  $("#js-signup-tab").toggleClass("hidden");
  $("#js-login-tab").toggleClass("hidden");
});

$(document).on("click", "#js-signup-tab-toggle", function(){
  $("#js-signup-tab").toggleClass("hidden");
  $("#js-login-tab").toggleClass("hidden");
});

// Sign in / Sign up modal close //
$(document).on("click", "#js-modal-close", function(){
  $(this).parents(".modal").remove();
});

// Form //
$(document).on("focus", "input", function(){
  $(this).toggleClass("input--focus");
});

$(document).on("blur", "input", function(){
  $(this).toggleClass("input--focus");
});



// // FORM //
// // Formfield on focus effect//
// $("input, textarea").on("focus", function() {
//   $(this).parent().addClass("formfield__input--focus");
// });
//
// // Formfield lose focus effect//
// $("input, textarea").on("blur", function() {
//   $(this).parent().removeClass("formfield__input--focus");
// });
//
// // FORM ERROR //
// function get_error(value){
//   var data = {};
//   data["value"] = value;
//   return $.ajax({
//     url: "/geterror/",
//     data: data
//   });
// }
// ////
//
//
// // NAVIGATION //
// // VERTICAL NAVIGATION //
// $(".js-nav-v-body-toggle").on("click", function() {
//   $("#js-nav-v-body").toggleClass("hidden");
//   $("body").toggleClass("no-scrollbar");
// });
//
// $(".js-nav-links-group-toggle").on("click", function() {
//   var element = $(this);
//   if (element.hasClass("js-account")) {
//     element.toggleClass("button--nav-active");
//   }
//   else{
//     element.children(".fa").toggleClass("fa-angle-right").toggleClass("fa-angle-down");
//   }
//   element.next().toggleClass("hidden");
// });
//
// $("#js-nav-search-toggle").on("click", function(){
//   $("#js-nav-search").toggleClass("hidden");
//   $("#js-nav-search-field").focus();
// })
//
//
// // ALERTS //
// function get_alert(message){
//   var data = {};
//   data["message"] = message;
//   return $.ajax({
//     url: "/getalert/",
//     data: data
//   });
// }
//
// function add_alert(alert){
//   $("body").append(alert);
//   $(".alert").hide().slideDown(500).delay(3000).slideUp(500,function(){$(this).remove();});
// }
// ////
//
// // Pop menu //
// $(document).on("click", "#js-pop-menu-toggle", function() {
//   $("#js-pop-menu").toggleClass("hidden");
// });
//
// $(document).on("click", ".js-select-option", function() {
//   var action = $(this).attr("data-action");
//   $("#js-post-create-action").text(action);
//   $("#js-pop-menu").toggleClass("hidden");
// });
//
// $(document).on("click", "#js-post-create", function(){
//   var action = $("#js-post-create-action").text();
//   $("#js-post-create-form").attr("action", "/posts/create/?action=" + action);
//   $("#js-submit-button").click();
// })
// // MODALS //
//
//
// function get_modal(template){
//   var data = {};
//   data["template"] = template;
//   return $.ajax({
//     url: "/getmodal/",
//     data: data
//   });
// }
// //
// function get_login_modal(url){
//   var data = {};
//   data["url"] = url;
//   return $.ajax({
//     url: "/getloginmodal/",
//     data: data
//   });
// }
//
// function get_post_modal(){
//   return $.ajax({
//     url: "/posts/modal/"
//   });
// }
//
// $(document).on("click", ".js-modal-close", function() {
//   $(this).parents(".modal").remove();
// });
//
// $(document).keyup(function(e) {
//   if (e.keyCode == 27) { // escape key maps to keycode `27`
//     $(".modal").remove();
//   }
// });
//
// $(".js-modal-post").on("click", function(){
//   get_post_modal().done(function(modal){
//     $("body").append(modal);
//     // $("#js-draft-publish-link").attr("href", url + "publish/");
//     $(".modal-wrapper").animate({top: 0});
//   });
// });
// ////
//
// LOGIN MODAL //
// $(".js-get-login-modal").on("click", function(){
//   var url = window.location.href;
//   get_login_modal(url).done(function(modal){
//     $("body").append(modal);
//     $(".modal__wrapper").animate({top: 0});
//   });
// });
//
// $(document).on("click", "#js-loginform-toggle", function(){
//   $("#js-signupform").toggleClass("hidden");
//   $("#js-loginform").toggleClass("hidden");
// });
//
// $(document).on("click", "#js-signupform-toggle", function(){
//   $("#js-loginform").toggleClass("hidden");
//   $("#js-signupform").toggleClass("hidden");
// });
////

//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
// //
// //
// // // loader
// // function get_loader(){
// //   return $.ajax({      // ajax GET to /getloader/
// //     url: "/getloader/",
// //   });
// // }
//
//
// // // List
// // function get_list_page(args){
// //   var list_page_url = args[0];
// //   return $.ajax({      // ajax GET to get_list_page
// //     url: list_page_url,
// //   });
// // }
// //
// // function add_list_page(args){
// //   var parent = args[0];
// //   var loader = args[1];
// //   var list_page = args[2];
// //   $(parent).find(".List-body").css("visibility","hidden");
// //   $('body').animate({scrollTop: $(parent).offset().top - 51}, 0, function(){
// //     $(parent).find(".List-header").after(loader);
// //     // $(parent).find(".List-header").after(loader);
// //     $(parent).find(".loader").fadeOut("fast",function(){
// //       $(this).next().remove();
// //       $(this).replaceWith(list_page);
// //     });
// //   });
// //
// // }
//
// //
// // $(document).on('click', '.btn-show', function(event) {
// //   event.preventDefault();
// //   var element = $(this);
// //   $(element).addClass("collapsed");
// //   $(element).next().removeClass("collapsed");
// //   var parent = $(element).parents(".ContentItem");
// //
// //   // $(element).hide().next().show();
// //   var item_comments_url = $(parent).attr("data-url") + "comments";
// //   });
// //
// //   $(document).on('click', '.btn-hide', function(event) {
// //     event.preventDefault();
// //     var element = $(this);
// //     var parent = $(element).parents(".ContentItem");
// //     $(element).addClass("collapsed");
// //     $(element).prev().removeClass("collapsed");
// //     // $(element).hide().prev().show();
// //     var item_comments_url = $(parent).attr("data-url") + "comments";
// //     });
// //
// //
// //
// //
// // // ContentItem pagination
// // function get_item_comments_page(args){
// //   var item_comments_url = args[0];
// //   var template = args[1];
// //   return $.ajax({
// //     url:item_comments_url,
// //     data: {
// //       template:template,
// //     }
// // });}
// //
// // function add_item_comments_page(args){
// //     var parent = args[0];
// //     var loader = args[1];
// //     var item_comments = args[2];
// //     $(parent).find(".ContentItem-comments-body").css("visibility","hidden");
// //     $('body').animate({scrollTop: $(parent).find(".ContentItem-actions").offset().top - 51}, 0, function(){
// //       $(parent).find(".ContentItem-comments-topbar").after(loader);
// //       $(parent).find(".loader").fadeOut("fast",function(){
// //         $(this).next().remove();
// //         $(this).replaceWith(item_comments);
// //       });
// //     });
// // }
// //
// // // ContentItem collapse
// // function get_item_comments(args){
// //   var item_comments_url = args[0];
// //   return $.ajax({
// //     url:item_comments_url,
// // });
// // }
// //
// //
// // $(document).on('click', '.btn-comment', function(event) {
// //   event.preventDefault();
// //   var element = $(this);
// //   var parent = $(element).parents(".ContentItem");
// //   var item_comments_url = $(parent).attr("data-url") + "comments";
// //   if ($(parent).find(".ContentItem-comments").length) {
// //     var ContentItem_comments = $(parent).find(".ContentItem-comments");
// //     $(ContentItem_comments).collapse('hide');
// //     $(ContentItem_comments).on('hidden.bs.collapse', function () {$(this).remove();});
// //     }
// //   else{
// //     var args = [item_comments_url];
// //     $.when(get_item_comments(args)).done(function(a1){
// //       var item_comments = a1;
// //       $(parent).append($(item_comments));
// //       $(parent).find(".ContentItem-comments").collapse('show');
// //       autosize($('textarea'));
// //   });
// // }});
//
//
//
//
//
// // user status
// function get_user_status(){
//   var user_status = $("#user-status").attr("data-user-status");
//   return user_status;
// }
// //
// //
// //
// //
// //
// //
// //
// // // contentitem likers modal
// // // Feature 3 Get and open post likers modal
// // $(document).on('click', '.btn-ContentItem-likers-count', function(event) {
// //   event.preventDefault();
// //   var element = $(this);
// //   var parent = $(element).parents(".ContentItem");
// //   var item_url = $(parent).attr("data-url");
// //   $.ajax({     // ajax GET to /posts/id/slug/likers
// //     url: item_url + "likers",
// //     success:function(data) {
// //       $("body").append(data);
// //       $(".modal").modal();
// //
// //     }});
// //   });
// //
// //
// //
// // // Feature 1 Like item
// // $(document).on('click', '.like-button', function(event) {
// //   event.preventDefault();
// //   var element = $(this);
// //   var parent = (element).parents(".ContentItem");
// //   var item_url = $(parent).attr("data-url");
// //   var user_status = $("#user_status").attr("data-user-status");
// //   if (user_status == "anonymous") {
// //     get_login_modal();
// //   }
// //   else if (user_status == "user"){
// //     $.ajax({  // ajax GET to /posts/id/slug/like
// //       url:item_url + "like",
// //       success:function(data) {
// //         if ($(element).hasClass("active")) {
// //           $(element).removeClass("active");
// //         }
// //         else{
// //           $(element).addClass("active");
// //         }
// //         $(parent).find(".ContentItem-likers-count").html(data.likes_count+" people liked this post.");
// //         $(parent).find(".ContentItem-actions-likers-count").html(data.likes_count);
// //       }
// //     });
// //   }
// // });
// //
// // // Feature 2 Dislike item
// // $(document).on('click', '.dislike-button', function(event) {
// //   event.preventDefault();
// //   var element = $(this);
// //   var parent = (element).parents(".ContentItem");
// //   var item_url = $(parent).attr("data-url");
// //   var user_status = $("#user_status").attr("data-user-status");
// //   if (user_status == "anonymous") {
// //     get_login_modal();
// //   }
// //   else if (user_status == "user"){
// //     $.ajax({  // ajax GET to /posts/id/slug/dislike
// //       url:item_url + "dislike",
// //       success:function(data) {
// //         if ($(element).hasClass("active")) {
// //           $(element).removeClass("active");
// //         }
// //         else{
// //           $(element).addClass("active");
// //         }
// //         $(parent).find(".ContentItem-actions-dislikers-count").html(data.dislikes_count);
// //       }
// //     });
// //   }
// // });
// //
//
//
// //
// //
// // function get_post_comments_count(args){
// //   var item_url = args[0];
// //   return $.ajax({   // ajax GET to /posts/id/slug/commentscount
// //     url:item_url + "commentscount",
// //   });
// // }
// //
// // function save_comment(args){
// //   var method = args[0];
// //   var item_url = args[1];
// //   var data = args[2];
// //   return $.ajax({  // ajax POST to /posts/id/slug/
// //     method: method,
// //     url: item_url,
// //     data: data,
// //   });
// // }
// //
// // function update_post_comments_count(args){
// //   var parent = args[0];
// //   var data = args[1];
// //   $(parent).find(".ContentItem-actions-comments-count").html(data);
// // }
// //
// //
// //
// //
// // function post_comments_add(callback,callback_args,callback_callback,args){
// //   var callback1 = callback[0];
// //   var callback2 = callback[1];
// //   var callback1_args = callback_args[0];
// //   var callback2_args = callback_args[1];
// //   var callback2_callback = callback_callback[0];
// //   var parent = args[0];
// //   var loader = args[1];
// //   var comments = args[2];
// //   $(parent).find(".ContentItem-comments-container").remove();
// //   $('body').animate({scrollTop: $(parent).find(".ContentItem-time").offset().top}, 0, function(){
// //     $(parent).find(".ContentItem-comments").append(loader);
// //     $(parent).find(".loader").fadeOut(3000,function(){
// //       $(this).replaceWith(comments);
// //       callback1(callback1_args);
// //       callback2(callback2_callback, callback2_args);
// //     });
// //   });
// // }
// //
// //
// //
// //
// //   $(document).on('submit', '.ContentItem-comments-form', function(event) {
// //     event.preventDefault();
// //     var element = $(this);
// //     var parent = (element).parents(".ContentItem");
// //     var item_url = $(parent).attr("data-url");
// //     var item_comments_url = item_url + "comments";
// //     var method = $(element).attr('method');
// //     var content = $(parent).find(".ContentItem-comments-form-textfield").val();
// //     var csrf_token = $(parent).find("[type='hidden']").val();
// //     var template = "template3";
// //     var data = {content:content, csrfmiddlewaretoken:csrf_token};
// //
// //     var args1 = [method,item_url,data];
// //     var args2 = [item_comments_url, template];
// //     var args3 = [item_url];
// //     $.when(get_loader(),save_comment(args1),get_post_comments(args2),get_post_comments_count(args3)).done(function(a1, a2, a3, a4){
// //       var loader = a1[0];
// //       var message = a2[0].message;
// //       var comments = a3[0];
// //       var comments_count = a4[0].post_comments_count;
// //       var callback = [update_post_comments_count,get_notification];
// //       var callback_args = [[parent,comments_count],[message]];
// //       var callback_callback = [add_notification];
// //       var args = [parent,loader,comments];
// //       post_comments_add(callback,callback_args,callback_callback,args);
// //     });
// //   });
//
//
//
//
// //     $(document).on('click', '.ContentItem-comments-form-textfield', function(event) {
// //       event.preventDefault();
// //       var element = $(this);
// //       var parent = (element).parents(".ContentItem")
// //       var user_status = get_user_status();
// //       if (user_status == "anonymous") {
// //         get_login_modal();
// //       }
// //       else {
// //         $(parent).find(".ContentItem-comments-form-collapse").collapse('show');
// //       }
// //     });
// //
// //
// //     $(document).on('click', '.btn-ContentItem-comments-form-cancel', function(event) {
// //       event.preventDefault();
// //       var element = $(this);
// //       var parent = $(element).parents(".ContentItem");
// //       $(parent).find(".ContentItem-comments-form-collapse").collapse('hide');
// //     });
// //
// //
// //
// //
// // // Feature 4 Close post likers modal
// // $(document).on('click', '.btn-closeModal', function(event) {
// // event.preventDefault();
// // var element = $(this);
// // var parent = $(element).parents(".modal");
// // $(parent).modal('hide');
// // });
// //
// // // Feature 5 Remove post likers modal once it is hidden
// // $(document).on('hidden.bs.modal', '.modal', function(event) {
// // event.preventDefault();
// // var element = $(this);
// // $(element).remove();
// // });
// //
// // // Feature 6 Get more post likers
// // $(document).on('click', '.btn-more', function() {
// // event.preventDefault();
// // var element = $(this);
// // var parent = $(element).parents(".modal");
// // var item_url = $(parent).attr("data-url");
// // var nextpage = $(parent).attr("data-nextpage");
// //
// // $.ajax({     // ajax GET to /posts/id/slug/likers?page=2
// // url: item_url + "likers/?page=" + nextpage,
// // beforeSend:get_loader(parent),
// // success:function(data) {
// // $("#post_likers_more_container").remove();
// // $("#post_likers_modal_body").append(data);
// // }});
// // });
// //
// // // Feature 7 Post likers modal follow buttons
// // $(document).on('click','.follow-button',function(){
// // event.preventDefault();
// // var element = $(this);
// // var parent = (element).parents(".ContentItem");
// // var item_url = $(parent).attr("data-url");
// // var ContentItem_modal_follow_status = $(parent).find(".ContentItem-modal-follow-status");
// // var ContentItem_modal_meta_StatusItem = $(parent).find(".ContentItem-modal-meta-StatusItem:last-child");
// // var follow_status = $(ContentItem_modal_follow_status).html();
// // var user_status = get_user_status();
// // if (user_status == "anonymous") {
// //   get_login_modal();
// // }
// // else {
// //   $.ajax({  // ajax GET to /profile/id/slug/follow
// //     url:item_url + "follow",
// //     data:{
// //       follow_status:follow_status,
// //     },
// //     success:function(data) {
// //       $(ContentItem_modal_follow_status).html(data.follow_status);
// //       $.ajax({
// //         url:item_url + "followerscount",  // ajax GET to /profile/id/slug/followerscount
// //         success:function(data){
// //           $(ContentItem_modal_meta_StatusItem).html(data.profile_followers_count+" Followers");
// //         }
// //       });
// //     }
// //   });
// // }
// // });
// //
// // // Feature mouseenter follow button
// // $(document).on('mouseenter','.follow-button',function(){
// // event.preventDefault();
// // var element = $(this);
// // var ContentItem_modal_follow_status = $(element).find(".ContentItem-modal-follow-status");
// // var user_status = get_user_status();
// // if (user_status == "anonymous") {
// //   event.preventDefault();
// // }
// // else{
// //   if ($(ContentItem_modal_follow_status).text() == "Followed") {
// //     $( ContentItem_modal_follow_status).text("Unfollow");
// //   }
// // }
// // });
// //
// // // mouseleave follow button
// // $(document).on('mouseleave','.follow-button',function(){
// // event.preventDefault();
// // var element = $(this);
// // var ContentItem_modal_follow_status = $(element).find(".ContentItem-modal-follow-status");
// // var user_status = get_user_status();
// // if (user_status == "anonymous") {
// //   event.preventDefault();
// // }
// // else{
// //   if ($(ContentItem_modal_follow_status).text() == "Unfollow") {
// //     $( ContentItem_modal_follow_status).text("Followed");
// //   }
// // }
// // });
