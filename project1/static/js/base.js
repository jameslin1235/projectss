function make_message(message){
  var message = '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+message+'</div>';
  return message;
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

function get_login_modal(){
  $.ajax({     // ajax GET to get and open login modal
    url: "/getloginmodal/",
    success:function(data) {
      $("body").append(data);
      $("#login_modal").modal();
    }});
  }

  // Feature 1 Close login modal
  $(document).on('click', '#login_modal_close_button', function(event) {
    event.preventDefault();
    $('#login_modal').modal('hide');
  });

  // Feature 2 Remove login modal once it is hidden
  $(document).on('hidden.bs.modal', '#login_modal', function(event) {
    event.preventDefault();
    var element = $(this);
    $(element).remove();
  });


  // Feature 1 Get nth page of paginated results
  $(document).on('click', '.page_button', function() {
    event.preventDefault();
    var element = $(this);
    var url = $(element).attr("href");

    $.ajax({     // ajax GET to get nth page
      url: url,
      success:function(data) {
        $(".list_page").replaceWith(data);
        // $("#profile_posts_select").val(option);
      }});
    });
