// SHOW PROFILE //
$(".js-profile-wrapper-get").on("click", function() {
  $(".profile-content").hide();
  $(".profile-wrapper").css("left","0");
  $("body").css("overflow","auto");
});
////

// SHOW PROFILE INFO //
$(".js-profile-info-toggle").on("click", function() {
  var element = $(this);
  $(".profile-briefinfo").toggleClass("hidden");
  $(".profile-info").toggleClass("hidden");
  $(element.children("span")[0]).toggleClass("fa-angle-down").toggleClass("fa-angle-up");
  $(element.children("span")[1]).text(function(i,text){
    return text === "Show" ? "Hide" : "Show";
    });
  });
  ////

  // SUBMIT PROFILE FORM //
  $(".js-profile-form").on("submit", function(event) {
    event.preventDefault();
    var element = $(this);
    var data = element.serialize();
    var message = "Profile updated";
    if ($(".formfield__error").length > 0){
      $(".formfield__error").remove();
    }
    submit_profile_form(data).done(function(response){
      if (Object.keys(response).length === 0 && response.constructor === Object){
        get_alert(message).done(function(alert){
          $("body").animate({scrollTop:0}, function(){add_alert(alert);});
        });
      }
      else{
        var count = 0;
        var length = Object.keys(response).length;
        function add_error(count){
          if (count < length){
            var value = response[Object.keys(response)[count]][0];
            get_error(value).done(function(error){
              $("input[name='" + Object.keys(response)[count] + "']").parents(".formfield").append(error);
              count++;
              add_error(count);
            });
          }
          else{
            $(".formfield__error").removeClass("hidden");
          }
        }
        add_error(count);
      }
    });
  });

  function submit_profile_form(data){
    return $.ajax({
      url: "/profile/edit/",
      data: data,
      method: "POST",
    });
  }
  ////

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

function render_uploaded_image(element){
  var file = element.files[0];
  var reader = new FileReader();
  reader.onload = function(event) {
    var img = new Image();
    img.onload = function(){
      var aspect_ratio = img.width / img.height;
      var width = 100;
      var height = width / aspect_ratio;
      document.getElementById("modal__canvas").getContext("2d").drawImage(img, 0, 0, width, height);
    }
    img.src = event.target.result;

  };
  reader.readAsDataURL(file);
}



$(document).on("click", ".js-profile-submit-edit-background-modal", function() {
  $(".js-profile-edit-background-form").submit();
});

$(".profile").on("submit", ".js-profile-edit-background-form", function(event) {
  event.preventDefault();
  var element = this;
  // var data = new FormData(element);
  var data = document.getElementById("canvas").toDataURL("image/jpeg");
  var message = "Profile background updated";
  submit_profile_background(data).done(function(response){
    if (response.hasOwnProperty("profile_background_url")){
      get_alert(message).done(function(alert){
        $("#profile_background").attr("src",response["profile_background_url"]);
        $(".Modal").remove();
        $("body").animate({scrollTop:0}, function(){add_alert(alert);});
      });
    }
    else{
    }
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
  $(".js-profile-avatar-edit").on("click", function() {
    $("#profile_avatar").click();
  });

  $("#profile_avatar").on("click",function(event){
    event.stopPropagation();
  });

  function validate_profile_avatar(element){

    var file = element.files[0];
    var img = new Image();
    img.onload = function () {
      if (img.width < 150 || img.height < 150){
        var message = "Avatar must be at least 150 by 150 pixels.";
        get_alert(message).done(function(alert){
          $("body").animate({scrollTop:0}, function(){add_alert(alert);});
        });
      }
      else{
        var width = 150;
        var height = (img.height/img.width) * width;
        var template = "profile_avatar_modal.html";
        get_modal(template).done(function(modal){
          $("body").append(modal);
          document.getElementById("modal__canvas").getContext("2d").drawImage(img, 0, 0, width, height);
          $(".modal__wrapper").animate({top: 0});
        });
      }
    }
    img.src = URL.createObjectURL(file);
  }

  $("#profile_avatar").on("change", function() {
    var element = this;
    validate_profile_avatar(element);
  });

  $(document).on("click", ".js-profile-avatar-submit", function() {
    $(".js-profile-avatar-form").submit();
  });

    $(".js-profile-avatar-form").on("submit", function(event) {
      event.preventDefault();
      var element = this;
      var filename = document.getElementById("profile_avatar").files[0].name;
      // console.log(filename);
      // console.log(document.getElementById("modal__canvas").toDataURL("image/jpeg"));
      var dataurl = document.getElementById("modal__canvas").toDataURL("image/jpeg").split(",")[1];
      var data = new FormData(element);
      data.append("dataurl", dataurl);
      data.append("filename", filename);
      submit_profile_avatar(data).done(function(response){
          // var message = "Profile avatar updated";
        // if (response.hasOwnProperty("profile_avatar_url")){
        //   get_alert(message).done(function(alert){
        //     $("#profile_avatar").attr("src",response["profile_avatar_url"]);
        //     $(".Modal").remove();
        //     $("body").animate({scrollTop:0}, function(){add_alert(alert);});
        //   });
        // }

      });
    });

    function submit_profile_avatar(data){
      return $.ajax({
        url: "/profile/editavatar/",
        data: data,
        method: "POST",
        processData: false,
        contentType: false
      });
    }
    ////
