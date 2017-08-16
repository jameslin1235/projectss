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
var bg_field = $("#js-bg-field");
var bg_modal = $("#js-bg-modal");
var bg_ctx = document.getElementById('js-bg-canvas').getContext('2d');

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

$("#js-bg-mask").on("click", function(){
  bg_field.click();
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

bg_field.on("change", function(){
  var file = this.files[0];
  var img = new Image();
  img.addEventListener("load", function() {
    bg_ctx.drawImage(img, 0, 0, 200, 200);
  }, false);
  img.src = window.URL.createObjectURL(file);
  bg_modal.toggleClass("hidden");
});

$("#js-avatar-modal-close").on("click", function(){
  avatar_modal.toggleClass("hidden");
  avatar_ctx.clearRect(0, 0, 200, 200);
  document.getElementById('js-avatar-form').reset();
});

$("#js-bg-modal-close").on("click", function(){
  bg_modal.toggleClass("hidden");
  bg_ctx.clearRect(0, 0, 200, 200);
  document.getElementById('js-bg-form').reset();
});

$("#js-edit-avatar").on("click", function(){
  $("#js-submit-avatar").click();
});

$("#js-edit-bg").on("click", function(){
  $("#js-submit-bg").click();
});
