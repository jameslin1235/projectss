
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});


var timeoutId;
var form = $("#form");
var save_status = $("#save-status");

$(".input").on("input", function(){
  save_status.text("Saving...");
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(function () {
    if (form.hasClass("js-mode-edit")) {
      tinyMCE.triggerSave();
      post_edit(form.attr("data-url")).done(function(response){
        save_status.text("Saved");
      });
    }
    else{
      tinyMCE.triggerSave();
      post_create().done(function(response){
      save_status.text("Saved");
      window.history.pushState("string", "Title", response["url"]);
      form.addClass("js-mode-edit").attr("data-url",response["url"]);
      });
    }
    }, 750);
});

tinymce.init({
  selector: "textarea",
  setup: function(editor) {
    editor.on('input', function(e) {
      save_status.text("Saving...");
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(function () {
        if (form.hasClass("js-mode-edit")) {
          tinyMCE.triggerSave();
          post_edit(form.attr("data-url")).done(function(response){
            save_status.text("Saved");
          });
        }
        else{
          tinyMCE.triggerSave();
          post_create().done(function(response){
          save_status.text("Saved");
          window.history.pushState("string", "Title", response["url"]);
          form.addClass("js-mode-edit").attr("data-url",response["url"]);
          });
        }
        }, 750);
    });
  },
  menubar: false,
  toolbar: [
    "formatselect | bold italic bullist numlist link blockquote alignleft aligncenter alignright spellchecker preview ",
    "strikethrough underline hr alignjustify forecolor pastetext removeformat charmap outdent indent undo redo"
  ],
  plugins: "lists spellchecker link preview hr textcolor paste charmap autoresize",
});


function post_create(){
  return $.ajax({
    method: "POST",
    url: "/p/create/",
    data: form.serialize()
  });
}

function post_edit(url){
  return $.ajax({
    method: "POST",
    url: url,
    data: form.serialize()
  });
}
