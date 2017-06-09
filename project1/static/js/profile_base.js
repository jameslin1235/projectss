// EDIT PROFILE //
$(".profile").on("click", ".js-profile-edit", function() {
  get_profile_form().done(function(profile_form){
    add_profile_form(profile_form);
  });
});

function get_profile_form(){
  return $.ajax({
    url: "/profile/edit/"
  });
}

function add_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  var profile_form = args[0];
  var container = $(".profile");
  $("body").animate({scrollTop:0}, function(){
    container.empty().append(profile_form);
  });
}
////

// GET PROFILE //
$(".profile").on("click", ".js-profile-get", function() {
  var template1 = "profile_header.html";
  var template2 = "profile_activity.html";
  $.when(get_profile_section(template1),get_profile_section(template2)).done(function(a1,a2){
    var profile_header = a1[0];
    var profile_body = a2[0];
    add_profile_section(profile_header,profile_body);
  });
});

function get_profile_section(){
  var args = Array.prototype.slice.call(arguments);
  var data = {};
  data["template"] = args[0];
  var profile_get_url = $("#profile_get_url").attr("href");
  return $.ajax({
    url: profile_get_url,
    data: data
  });
}

function add_profile_section(){
  var args = Array.prototype.slice.call(arguments);
  var profile_header = args[0];
  var profile_body = args[1];
  var container = $(".profile");
  $("body").animate({scrollTop:0}, function(){
    container.empty().append(profile_header).append(profile_body);
  });
}
////

// SUBMIT PROFILE //
$(".profile").on("submit", ".js-profile-form", function(event) {
  event.preventDefault();
  var element = $(this);
  var data = element.serialize();
  var message = "Profile updated";
  if ($(".card__formfielderror").length > 0){
    $(".card__formfielderror").remove();
  }
  submit_profile_form(data).done(function(response){
    if (Object.keys(response).length === 0 && response.constructor === Object){
      get_alert(message).done(function(alert){
        $("body").animate({scrollTop:0}, function(){add_alert(alert);});
      });
    }
    else{
      var i = 0;
      var length = Object.keys(response).length;
      function add_error(){
        var args = Array.prototype.slice.call(arguments);
        var i = args[0];
        if (i < length){
          var value = response[Object.keys(response)[i]][0];
          get_error(value).done(function(error){
            $("input[name='" + Object.keys(response)[i] + "']").parents(".card__formfieldvalue").after(error);
            i++;
            add_error(i);
          });
        }
        else{
          $(".card__formfielderror").toggleClass("is--hidden");
        }
      }
      add_error(i);
    }
  });
});

function submit_profile_form(){
  var args = Array.prototype.slice.call(arguments);
  var data = args[0];
  return $.ajax({
    url: "/profile/edit/",
    data: data,
    method: "POST",
  });
}

// EDIT PROFILE BACKGROUND //
$(".profile").on("click", ".js-profile-edit-background", function() {
  $("#id_background").click();
});

$(".profile").on("change", "#id_background", function() {
  var element = this;
  var template = "profile_edit_background_modal.html";
  get_modal(template).done(function(modal){
    $("body").append(modal);
    render_uploaded_image(element);
    $(".Modal__content").animate({top: 0});
  });
});

function render_uploaded_image(){
  var args = Array.prototype.slice.call(arguments);
  var element = args[0];
  var file = element.files[0];
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
  var element = this;
  var data = new FormData(element);
  var message = "Profile background updated";

  submit_profile_background(data).done(function(response){
    if (Object.keys(response).length === 0 && response.constructor === Object){
      get_alert(message).done(function(alert){
        $("body").animate({scrollTop:0}, function(){add_alert(alert);});
      });
    }
  });


  ,get_alert(message)).done(function(a1,a2){
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

  function submit_profile_background(){
    var args = Array.prototype.slice.call(arguments);
    var data = args[0];
    return $.ajax({
      url: "/profile/editbackground/",
      data: data,
      method: "POST",
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
