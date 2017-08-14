tinymce.init({
  selector: "#js-textarea",
  setup: function(editor) {
    editor.on('input', function(e) {
      tinyMCE.triggerSave();
    });
  },
  menubar: false,
  toolbar: [
    "formatselect | bold italic bullist numlist link blockquote alignleft aligncenter alignright spellchecker preview ",
    "strikethrough underline hr alignjustify forecolor pastetext removeformat charmap outdent indent undo redo"
  ],
  plugins: "lists spellchecker link preview hr textcolor paste charmap autoresize",
});

var url = $("#profile-edit").attr("data-url");
var avatar_field = $("#js-avatar-field");
var avatar_modal = $("#js-avatar-modal");
var avatar_ctx = document.getElementById('js-avatar-canvas').getContext('2d');

$("#js-form").on("submit", function(e){
  e.preventDefault();
  var data = $(this).serialize();
  $.ajax({
    method: "PATCH",
    url: url,
    data: data
  }).done(function( response ) {
    window.location.href = url;
  });
});

$("#js-avatar-mask").on("click", function(){
  avatar_field.click();
});

avatar_field.on("change", function(){
  var file = this.files[0];
  var img = new Image();
  img.addEventListener("load", function() {
    avatar_ctx.drawImage(img, 0, 0, 200, 200);
  }, false);
  img.src = window.URL.createObjectURL(file);
  avatar_modal.toggleClass("hidden");
});

$("#js-avatar-modal-close").on("click", function(){
  avatar_modal.toggleClass("hidden");
  avatar_ctx.clearRect(0, 0, 200, 200);
  document.getElementById('js-avatar-form').reset();
});

// $("#js-edit-avatar").on("click", function(){
//   var data = new FormData();
//   data.append("avatar", avatar_field[0].files[0]);
//   $.ajax({
//     method: "POST",
//     url: url,
//     data: data,
//     processData: false,
//     contentType: false
//   }).done(function( response ) {
//     // window.location.href = url;
//   });
// });
