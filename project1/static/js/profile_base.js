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
$(".js-profile-background-edit").on("click", function() {
  $(".js-profile-background-field").click();
});

$(".js-profile-background-field").on("change", function() {
  var element = this;
  validate_profile_background(element);
});

function validate_profile_background(element){
  var file = element.files[0];
  var img = new Image();
  img.onload = function () {
    var width = img.width;
    var height = img.height;
    if (width < 1200){
      var message = "Image width must be 1200 pixels or more.";
      get_alert(message).done(function(alert){
        $("body").animate({scrollTop:0}, function(){add_alert(alert);});
    });
    }
    else{
      var new_width = 1200; // image can be resized to 1200px
      var new_height = (height/width) * new_width;
      if (new_height < 300){
        var message = "Resized image height must be 300 pixels or more.";
        get_alert(message).done(function(alert){
          $("body").animate({scrollTop:0}, function(){add_alert(alert);});
      });
    }
      else{
        var template = "profile_background_modal.html";
        get_modal(template).done(function(modal){
          $("body").append(modal);
          document.getElementById("modal__canvas").width = new_width;
          document.getElementById("modal__canvas").height = new_height;
          document.getElementById("modal__canvas").getContext("2d").drawImage(img, 0, 0, new_width, new_height);
          $(".modal__wrapper").animate({top: 0});
      });
    }
  }}
  img.src = URL.createObjectURL(file);
}

// function render_uploaded_image(element){
//   var file = element.files[0];
//   var reader = new FileReader();
//   reader.onload = function(event) {
//     var img = new Image();
//     img.onload = function(){
//       var aspect_ratio = img.width / img.height;
//       var width = 100;
//       var height = width / aspect_ratio;
//       document.getElementById("modal__canvas").getContext("2d").drawImage(img, 0, 0, width, height);
//     }
//     img.src = event.target.result;
//
//   };
//   reader.readAsDataURL(file);
// }

$(document).on("click", ".js-profile-background-submit", function() {
  $(".js-profile-background-form").submit();
});


$(".js-profile-background-form").on("submit", function(event) {
  event.preventDefault();
  var element = this;
  var dataurl = document.getElementById("modal__canvas").toDataURL("image/jpeg").split(",")[1];
  var filename = document.getElementsByClassName("js-profile-background-field")[0].files[0].name;
  var data = new FormData(element);
  data.append("dataurl", dataurl);
  data.append("filename", filename);
  submit_profile_background(data).done(function(response){
    var message = "Profile background updated";
    get_alert(message).done(function(alert){
      $(".js-profile-background").attr("src",response["profile_background_url"]);
      $(".modal").remove();
      $("body").animate({scrollTop:0}, function(){add_alert(alert);});
    });
  });
});

// $(".profile").on("submit", ".js-profile-edit-background-form", function(event) {
//   event.preventDefault();
//   var element = this;
//   // var data = new FormData(element);
//   var data = document.getElementById("canvas").toDataURL("image/jpeg");
//   var message = "Profile background updated";
//   submit_profile_background(data).done(function(response){
//     if (response.hasOwnProperty("profile_background_url")){
//       get_alert(message).done(function(alert){
//         $("#profile_background").attr("src",response["profile_background_url"]);
//         $(".Modal").remove();
//         $("body").animate({scrollTop:0}, function(){add_alert(alert);});
//       });
//     }
//     else{
//     }
//   });
// });

  // function submit_profile_background(){
  //   var args = Array.prototype.slice.call(arguments);
  //   var data = args[0];
  //   return $.ajax({
  //     url: "/profile/editbackground/",
  //     data: data,
  //     method: "POST",
  //     processData: false,
  //     contentType: false,
  //   });
  // }

  function submit_profile_background(data){
    return $.ajax({
      url: "/profile/editbackground/",
      data: data,
      method: "POST",
      processData: false,
      contentType: false
    });
  }
  ////

  // EDIT PROFILE AVATAR //
  $(".js-profile-avatar-edit").on("click", function() {
    $(".js-profile-avatar-field").click();
  });

  $(".js-profile-avatar-field").on("click",function(event){
    event.stopPropagation();
  });

  function validate_profile_avatar(element){
    var file = element.files[0];
    var img = new Image();
    img.onload = function () {
      var width = img.width;
      var height = img.height;
      if (width < 300){
        var message = "Image width must be 300 pixels or more.";
        get_alert(message).done(function(alert){
          $("body").animate({scrollTop:0}, function(){add_alert(alert);});
      });
      }
      else{
        var new_width = 300; // image can be resized to 300px
        var new_height = (height/width) * new_width;
        if (new_height < 150){
          var message = "Resized image height must be 150 pixels or more.";
          get_alert(message).done(function(alert){
            $("body").animate({scrollTop:0}, function(){add_alert(alert);});
        });
      }

        else{
          var template = "profile_avatar_modal.html";
          get_modal(template).done(function(modal){
            $("body").append(modal);
            document.getElementById("modal__canvas").width = new_width;
            document.getElementById("modal__canvas").height = new_height;
            document.getElementById("modal__canvas").getContext("2d").drawImage(img, 0, 0, new_width, new_height);
            $(".modal__wrapper").animate({top: 0});
        });
      }
    }}
    img.src = URL.createObjectURL(file);
  }

  $(".js-profile-avatar-field").on("change", function() {
    var element = this;
    validate_profile_avatar(element);
  });

  $(document).on("click", ".js-profile-avatar-submit", function() {
    $(".js-profile-avatar-form").submit();
  });

    // $(".js-profile-avatar-form").on("submit", function(event) {
    //   event.preventDefault();
    //   var element = this;
    //   var dataurl = document.getElementById("modal__canvas").toDataURL("image/jpeg").split(",")[1];
    //   var filename = document.getElementsByClassName("js-profile-avatar-field")[0].files[0].name;
    //   var data = new FormData(element);
    //   data.append("dataurl", dataurl);
    //   data.append("filename", filename);
    //   submit_profile_avatar(data).done(function(response){
    //     var message = "Profile avatar updated";
    //     get_alert(message).done(function(alert){
    //       $(".js-profile-avatar").attr("src",response["profile_avatar_url"]);
    //       $(".modal").remove();
    //       $("body").animate({scrollTop:0}, function(){add_alert(alert);});
    //     });
    //   });
    // });

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
