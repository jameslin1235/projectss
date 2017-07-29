tinymce.init({
  selector: "#textarea",
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


// $(".js-submit").on("click", function(){
//
//   // if (tinyMCE.get("textarea").getContent() == "") {
//   //   console.log('w');
//   //   $("#js-required").removeClass("hidden");
//   //   $(".js-form").submit(function(e){
//   //     e.preventDefault();
//   //   });
//   // }
//
// });

$("#textarea").on("invalid", function(e){
  e.preventDefault();
  $("#js-required").removeClass("hidden");
});
