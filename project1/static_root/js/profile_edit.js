
// EDIT PROFILE AVATAR //
$("#js-profile-avatar-edit").on("click", function(event) {
  $("#js-profile-avatar-filefield").click();
});

$("#js-profile-avatar-filefield").on("click", function(event) {
  event.stopPropagation();
});

$("#js-profile-avatar-filefield").on("change", function() {
  var element = this;
  validate_profile_avatar(element);
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
      if (new_height > height){
        var message = "Resized image height must not be greater than original height.";
        get_alert(message).done(function(alert){
          $("body").animate({scrollTop:0}, function(){add_alert(alert);});
        });
      }
      else if (new_height < 150){
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

  $(document).on("click", "#js-profile-avatar-submit", function() {
    $("#id_avatar_dataurl").val(document.getElementById("modal__canvas").toDataURL("image/jpeg").split(",")[1]);
    $("#id_avatar_filename").val(document.getElementById("js-profile-avatar-filefield").files[0].name);
    $("#js-profile-avatar-form").submit();
   });
  ////

  // EDIT PROFILE BACKGROUND //
  $("#js-profile-background-edit").on("click", function(event) {
    $("#js-profile-background-filefield").click();
  });

  $("#js-profile-background-filefield").on("click", function(event) {
    event.stopPropagation();
  });

  $("#js-profile-background-filefield").on("change", function() {
    var element = this;
    validate_profile_background(element);
  });

  function validate_profile_background(element){
    var file = element.files[0];
    console.log(file)
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
        if (new_height > height){
          var message = "Resized image height must not be greater than original height.";
          get_alert(message).done(function(alert){
            $("body").animate({scrollTop:0}, function(){add_alert(alert);});
          });
        }
        else if (new_height < 300){
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

    $(document).on("click", "#js-profile-background-submit", function() {
      $("#id_background_dataurl").val(document.getElementById("modal__canvas").toDataURL("image/jpeg").split(",")[1]);
      $("#id_background_filename").val(document.getElementById("js-profile-background-filefield").files[0].name);
      $("#js-profile-background-form").submit();
     });
    ////
