// EDIT PROFILE //
$(".profile").on("click", ".js-profile-edit", function() {
  var element = $(this);
  var profile_edit_url = element.attr("data-url");
  var parent = element.parents(".profile");
  $.when(get_profile_form(profile_edit_url)).done(function(a1){
    var profile_form = a1;
    add_profile_form(parent,profile_form);
  });
});

function get_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  profile_edit_url = args[0]
  return $.ajax({
    url: profile_edit_url,
  });
}

function add_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  parent = args[0];
  profile_form = args[1];
  parent.empty().append(profile_form);
}
////

// GET PROFILE //
$(".profile").on("click", ".js-profile-get", function() {
  var element = $(this);
  var profile_get_url = element.attr("data-url");
  var parent = element.parents(".profile");
  var template1 = "profile_header";
  var template2 = "profile_body";
  $.when(get_profile_section(profile_get_url,template1),get_profile_section(profile_get_url,template2)).done(function(a1,a2){
    var profile_header = a1[0];
    var profile_body = a2[0];
    add_profile_section(parent,profile_header,profile_body);
  });
});

function get_profile_section(){
  var args = Array.prototype.slice.call(arguments);
  profile_get_url = args[0]
  template = args[1]
  return $.ajax({
    url: profile_get_url,
    data: {
      template:template,
    }
  });
}

function add_profile_section(){
  var args = Array.prototype.slice.call(arguments);
  parent = args[0];
  profile_header = args[1];
  profile_body = args[2];
  parent.empty().append(profile_header).append(profile_body);
}
////

// SUBMIT PROFILE //
$(".profile").on("submit", ".js-profile-form", function(event) {
  event.preventDefault();
  var element = $(this);
  var profile_submit_url = element.attr("action");
  var data = element.serialize();
  var method = element.attr("method");
  var parent = (element).parents(".profile");
  var message = "Profile updated";
  $.when(submit_profile_form(profile_submit_url,data,method),get_alert(message)).done(function(a1,a2){
    var message = a2[0];
    $("body").animate({scrollTop:0}, function(){
      add_alert(message);
    });
  });
});

function submit_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  profile_submit_url = args[0];
  data = args[1];
  method = args[2];
  return $.ajax({
    url: profile_submit_url,
    data: data,
    method: method,
  });
}
////

// EDIT PROFILE BACKGROUND //
$(".profile").on("click", ".js-profile-edit-background", function() {
  $(this).parent(".card__background").find("input[type='file']").click();
});

$(".profile").on("change", "#id_background", function() {
  var element = $(this);
  var template = "profile_edit_background_modal.html";
  $.when(get_modal(template)).done(function(a1){
    var modal = a1;
    $("body").append(modal);
    render_uploaded_image(element[0]);
    $(".Modal__content").animate({top: 0});
  });
});

function render_uploaded_image(){
  var args = Array.prototype.slice.call(arguments);
  var element = args[0];
  var files = element.files;
  var file = files[0];
  var reader = new FileReader();
  reader.onload = function(event) {
    var src = event.target.result;
    $(".Modal__body").append('<img class="Modal__bodyimage" src="' + src + '" alt="Profile Image">');
  };
  reader.readAsDataURL(file);
}

$(document).on("click", ".js-profile-submit-edit-background-modal", function() {
  $(".js-profile-edit-background-form").submit();
});

$(".profile").on("submit", ".js-profile-edit-background-form", function(event) {
  event.preventDefault();
  var element = $(this);
  var url = element.attr("action");
  var data = new FormData(element[0]);
  var method = element.attr("method");
  var message = "Profile background updated";
  $.when(submit_profile_files(url,data,method),get_alert(message)).done(function(a1,a2){
    var profile_background_url = a1[0]["profile_background_url"];
    var message = a2[0];
    $(".Modal").remove();
    element.parents(".card__background").find("img").attr("src",profile_background_url);
    $("body").animate({scrollTop:0},
      function(){
        add_alert(message);
      });
    });
  });

  function submit_profile_files(){
    var args = Array.prototype.slice.call(arguments);
    url = args[0];
    data = args[1];
    method = args[2];
    return $.ajax({
      url: url,
      data: data,
      method: method,
      processData: false,
      contentType: false,
    });
  }
  ////

  // EDIT PROFILE AVATAR //
  $(".profile").on("click", ".js-profile-edit-avatar", function() {
    $(this).find("input[type='file']").click();
  });

  $(".profile").on("click", "#id_avatar", function(event){
    event.stopPropagation();
  });

  $(".profile").on("change", "#id_avatar", function() {
    var element = $(this);
    var template = "profile_edit_avatar_modal.html";
    $.when(get_modal(template)).done(function(a1){
      var modal = a1;
      $("body").append(modal);
      render_uploaded_image(element[0]);
      $(".Modal__content").animate({top: 0});
    });
  });

  $(document).on("click", ".js-profile-submit-edit-avatar-modal", function() {
    $(".js-profile-edit-avatar-form").submit();
  });

  $(".profile").on("submit", ".js-profile-edit-avatar-form", function(event) {
    event.preventDefault();
    var element = $(this);
    var url = element.attr("action");
    var data = new FormData(element[0]);
    var method = element.attr("method");
    var message = "Profile avatar updated";
    $.when(submit_profile_files(url,data,method),get_alert(message)).done(function(a1,a2){
      var profile_avatar_url = a1[0]["profile_avatar_url"];
      var message = a2[0];
      element.parents(".card__avatar").find("img").attr("src",profile_avatar_url);
      $(".Modal").remove();
      $("body").animate({scrollTop:0},
        function(){
          add_alert(message);
        });
      });
    });
    ////
