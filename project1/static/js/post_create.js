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

$("#js-input").on("invalid", function(e){
  e.preventDefault();
  $(this).after("<span class='js-error error'>Title can't be blank.</span>");
});

$("#js-textarea").on("invalid", function(e){
  e.preventDefault();
  $("#mceu_24").after("<span class='js-error error'>Content can't be blank.</span>");
});

$(".js-submit").on("click", function(){
  if ($(".js-error").length) {
    $(".js-error").remove();
  }
});
