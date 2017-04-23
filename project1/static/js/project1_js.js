// post_list.html
var pag1 = '<li class="disabled"><span>&laquo;</span></li>';
var pag2 = '<li class="disabled"><span>&raquo;</span></li>';

function make_message(){
  var message = '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Comment created.</div>';
  return message;
}

function make_post_list_pag(id){
  var post_list_pag = '<div id="post_list_pag_'+id+'"><ul id="post_list_pag_ul_'+id+'" class="pagination"></ul></div>';
  return post_list_pag;
}

function make_post_list_page(data, i){
  var post_list_page = '<div class="media"><div class="media-left"><a href="'+data.list5[i]+'"><img class="media-object" src="'+data.list1[i]+'" alt="..." width="64px" height="64px"></a></div><div class="media-body"><a class="media-heading" href="'+data.list5[i]+'">'+data.list2[i]+'</a><p>'+ data.list3[i]+'</p><p>'+data.list4[i]+'</p></div></div>';
  return post_list_page;
}

function make_post_list_comment_list(data,id){
  var post_list_comment_list = '<div id="post_list_comment_list_'+id+'"><div class="media"><div class="media-left"><a href="'+data.profile_url+'"><img class="media-object" src="'+data.avatar+'" alt="..." width="64px" height="64px"></a></div><div class="media-body"><a class="media-heading" href="'+data.profile_url+'">'+data.username+'</a><p>'+ data.content+'</p><p>'+data.date_created+'</p></div></div></div>'
  return post_list_comment_list;
}

function make_comment(data){
  var comment = '<div class="media"><div class="media-left"><a href="'+data.profile_url+'"><img class="media-object" src="'+data.avatar+'" alt="..." width="64px" height="64px"></a></div><div class="media-body"><a class="media-heading" href="'+data.profile_url+'">'+data.username+'</a><p>'+ data.content+'</p><p>'+data.date_created+'</p></div></div>';
  return comment;
}

function paginate(data,id,url) {
  if (data.has_previous) {
    ppn = data.number-1;
    $("#post_list_pag_ul_"+id).append('<li><a class="page_button" href="'+url+'?page='+ppn+'" data-id="'+id+'"data-url="'+url+'">&laquo;</a></li>');
  }
  else {
    $("#post_list_pag_ul_"+id).append(pag1);
  }
  for (var x = 1; x < data.page_range+1; x++) {
    if (data.number == x) {
      $("#post_list_pag_ul_"+id).append('<li class="active"><span>'+x+'<span class="sr-only">(current)</span></span></li>');

    }
    else {
      $("#post_list_pag_ul_"+id).append('<li><a class="page_button" href="'+url+'?page='+x+'" data-id="'+id+'" data-url="'+url+'">'+x+'</a></li>');
    }
  }
  if (data.has_next) {
    npn = data.number+1;
    $("#post_list_pag_ul_"+id).append('<li><a class="page_button" href="'+url+'?page='+npn+'" data-id="'+id+'" data-url="'+url+'">&raquo;</a></li>');
  }
  else {
    $("#post_list_pag_ul_"+id).append(pag2);
  }
}

// Feature 1
$(document).on('click', '.like_button', function(event) {
  event.preventDefault();
  var element = $(this);
  if ($("#logged_in").attr("data-logged-in")=="True") {
    if($(element).attr("data-liked")=="False"){

      $.ajax({
        url:$(element).attr("data-post") + "like",
        success:function(data) {
          $(element).html('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ' + data.like_count);
          $(element).attr("data-liked","True");
        }
      })
    }
    else{
      $.ajax({
        url:$(element).attr("data-post") + "like",
        data:{ unlike: "unlike" },
        success:function(data) {
          $(element).html('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ' + data.like_count);
          $(element).attr("data-liked","False");
        }
      })
    }

  }
  else{
    $('#myModal').modal()
  }
});

// Feature 2
$(document).on('click', '.dislike_button', function(event) {
  event.preventDefault();
  var element = $(this);
  if ($("#logged_in").attr("data-logged-in")=="True") {

    if($(element).attr("data-disliked")=="False"){

      $.ajax({
        url:$(element).attr("data-post") + "dislike",
        success:function(data) {
          $(element).html('<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ' + data.dislike_count);
          $(element).attr("data-disliked","True");
        }
      })
    }
    else{
      $.ajax({
        url:$(element).attr("data-post") + "dislike",
        data:{ undislike: "undislike" },
        success:function(data) {
          $(element).html('<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ' + data.dislike_count);
          $(element).attr("data-disliked","False");
        }
      })
    }

  }
  else{
    $('#myModal').modal()
  }
});

// Feature 3
$(document).on('click', '.comment_button', function(event) {
  event.preventDefault();
  var element = $(this);
  var id = $(element).attr("data-id");
  $("#comment_collapse_"+id).collapse("toggle");
});

// Feature 4
$(document).on('click', '.bookmark_button', function(event) {
  event.preventDefault();
  var element = $(this);
  if ($("#logged_in").attr("data-logged-in")=="True") {

    alert("hello");
  }
  else{
    $('#myModal').modal()
  }
});

// Feature 4
$(document).on('click', '.comment_form_field', function(event) {
  event.preventDefault();
  var element = $(this);
  if ($("#logged_in").attr("data-logged-in")=="True") {
    var id = $(element).attr("data-id");
    $("#commentform_collapse_"+id).collapse("toggle");
  }
  else{
    $('#myModal').modal()
  }
});


// Feature 5
$(document).on('submit', '.comment_form', function(event) {
  event.preventDefault();
  var element = $(this);
  var id = $(this).attr("data-id");
  var url = $(this).attr("data-url");

  $.ajax({
    type:  $(element).attr('method'),
    url:  url,
    data:  {
      content: $("#comment_form_textfield_"+id).val(),
      csrfmiddlewaretoken:'{{ csrf_token }}',
      id:id,
    },
    success:function(data) {
      if (data.success) {
        $("#comment_button_"+id).html('<span class="glyphicon glyphicon-comment" aria-hidden="true"></span> '+data.comments_count);
        $("#comments_count_"+id).html(data.comments_count + " Comments");
        $("#comment_form_textfield_"+id).val("");
        $('#comment_page_header_'+id).after(make_message());

        if($('#post_list_comment_list_'+id).length){
          if ($(element).attr("data-pagenum") == 1) {
            $('#post_list_comment_list_'+id).prepend(make_comment(data));
            $('#post_list_pag_'+id).remove();
            $('#post_list_comment_list_'+id).after(make_post_list_pag(id));
            paginate(data,id,url);
            if (data.comments_count>5) {
              $("#post_list_comment_list_"+id).children().last().remove();
            }
          }
          else{
            $.ajax({
              url:url,
              success:function(data) {
                $("#post_list_comment_list_"+id).remove();
                $("#post_list_pag_"+id).remove();
                $("#comment_form_container_"+id).before('<div id="post_list_comment_list_'+id+'"></div>');
                for (var i = 0; i < data.comment_count; i++) {
                  $("#post_list_comment_list_"+id).append(make_post_list_page(data, i));
                }
                $("#post_list_comment_list_"+id).after(make_post_list_pag(id));
                paginate(data,id,url);
                $(element).attr("data-pagenum",data.number);
              }
            })
          }

        }
        else{
          if($(element).attr("data-pagenum") == 1){
            if(data.comments_count == 1){
              $("#comment_form_container_"+id).before(make_post_list_comment_list(data,id));
              $("#post_list_comment_list_"+id).after(make_post_list_pag(id));
              paginate(data,id,url);
              $("#no_comments_"+id).remove();

            }
            else{
              $("#post_list_comment_list_"+id).prepend(make_comment(data));
              $("#post_list_pag_"+id).remove();
              $("#post_list_comment_list_"+id).after(make_post_list_pag(id));
              paginate(data,id,url);

            }
            if(data.comments_count>5){
              $("#post_list_comment_list_"+id).children().last().remove();
            }
          }
          else{
            $.ajax({
              url:url,
              success:function(data) {
                $("#post_list_comment_list_"+id).remove();
                $("#post_list_pag_"+id).remove();
                $("#comment_form_container_"+id).before('<div id="post_list_comment_list_'+id+'"></div>');
                for (var i = 0; i < data.comment_count; i++) {
                  $("#post_list_comment_list_"+id).append(make_post_list_page(data, i));
                }
                $("#post_list_comment_list_"+id).after(make_post_list_pag(id));
                paginate(data,id,url);
                $(element).attr("data-pagenum",data.number);
              }
            })
          }
        }
      }
      else{
        alert("wrong");
      }

    },
  });
})

// Feature 6
$(document).on('click', '.page_button', function() {
  event.preventDefault();
  var element = $(this);
  var id = $(this).attr("data-id");
  var url = $(this).attr("data-url");
  $.ajax({
    url:$(element).attr("href"),
    success:function(data) {
      $("#post_list_comment_list_"+id).remove();
      $("#post_list_pag_"+id).remove();
      $("#comment_form_container_"+id).before('<div id="post_list_comment_list_'+id+'"></div>');
      for (var i = 0; i < data.comment_count; i++) {
        $("#post_list_comment_list_"+id).append(make_post_list_page(data, i));
      }
      $("#post_list_comment_list_"+id).after(make_post_list_pag(id));
      paginate(data,id,url);
      $("#comment_form_"+id).attr("data-pagenum",data.number);
    }});
  });
