  //좋아요 손가락
//fas: on  far:off
    $('i.fa-thumbs-up').click(function(){
  $(this).toggleClass("fas").toggleClass("far")
})

 $('i.fa-star').click(function(){
  $(this).toggleClass("fas").toggleClass("far")
})



  $('i.like').click(function(){
    var pk = $(this).attr('name').substr(9)
    var liketype=$(this).attr('name').substr(0,3)
      // cop:CodePost coc:CodeComment cdp:CodePost cdc:CodeComment
      //ex) cop-3 cdc-30
    $.ajax({
     type: "POST",
      url: "{% url 'comp:uploadlike' %}",
      data: {'pk': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}', 'liketype':liketype},
      dataType: "json",

      success: function(response){
        $("#"+liketype+"-likecount-"+pk).html(response.like);
      },


      error: function(request, status, error){ // 통신 실패시 - 로그인 페이지 리다이렉트
        window.location.replace("/accounts/login/")
          //alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
          },
    })
  })
