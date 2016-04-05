$(document).ready(function(){
    
    
    
    
    
    function getCookie(cname){
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++){
	    var c = ca[i].trim();
	    if (c.indexOf(name)==0) return c.substring(name.length,c.length);
	  }
	return "";
    }
    

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

    
    
    
    
    
//    tool tips

    $('.tooltips').tooltip();

//    popovers

    $('.popovers').popover({html:true});

    
    
    
    function colorHashtags(id) {
	var str = $("#"+id).html();
	var re = /(\A|\s|^)#(\w+)/g; 
	var replaceText = str.replace(re, function(a,b,c){
	    //console.log(b+'#<a class="hashtagTweet" href="/search/?q='+ c +'">'+ c +'</a>');
	    return b+'<a class="hashtagTweet" href="/search/?q='+ c +'">#'+ c +'</a>'
	});
	//console.log(str);
	//console.log(replaceText);
	$("#"+id).html(replaceText);
	
    }
    
    function colorAtSigns(id) {
	var str = $("#"+id).html();
	var re = /(\A|\s|^)@(\w+)/g; 
	var replaceText = str.replace(re, function(a,b,c){
	    //console.log(b+'<span style="color:#ff0f0f;">@'+ c +'</span>');
	    return b+'<a class="hashtagTweet" href="#">@'+ c +'</span>'
	});
	//console.log(str);
	//console.log(replaceText);
	$("#"+id).html(replaceText);
	
    }
    
    function colorWebLinks(id) {
	var str = $("#"+id).html();
	var re = /(\A|\s|^)(\S*)(http|https|www\.|\.com|\.net|\.org|\.gov|\.biz|\.edu|\.us|\.ect|\.int|\.ru|\.mil|\.tv)(\S*)/g; 
	var replaceText = str.replace(re, function(a,b){
	    var strippedLink = a.trim();
	    var hiddenLink;
	    if (strippedLink.substring(0,4)!="http") {
		hiddenLink = "http://"+strippedLink;
	    }else{hiddenLink = strippedLink;}
	    //console.log(b+'<a class="colorLink" href="'+ hiddenLink +'" target="newLink">'+ strippedLink +'</a>');
	    return b+'<a class="colorLink" href="'+ hiddenLink +'" target="newLink">'+ strippedLink +'</a>'
	});
	//console.log(str);
	//console.log(replaceText);
	$("#"+id).html(replaceText);
	
    }
    
    $('.tweet-text').each(function(){
        var id = $(this).attr('id');
        colorHashtags(id);
        colorAtSigns(id);
        colorWebLinks(id);
    });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    $(".launchTweet").click(function(){
        $("#tweet-popup").modal('show');
    });
    
    
    /************************* Enter Tweet **********************************************************************************/
    $("#tweetRichBox").keyup(function(){
	if ($(this).html().length == 0 || $(this).html().length > 140) {
	    $("#tweetSubmit").addClass("disabled");
	}
        else{
	    $("#tweetSubmit").removeClass('disabled');
	}
        if ($(this).html().length > 140) {
	    $("#number-counter").addClass("text-danger").removeClass("text-primary");
            if ($(this).html().indexOf("<b>") == -1 || $(this).html().indexOf("<strong>") == -1) {
                document.execCommand('bold', 0, null);
            }
	}
        else{
	    $("#number-counter").removeClass('text-danger').addClass("text-primary");
	}
        
	$("#number-counter").text(140 - $(this).html().length);
    });
    
    
    
    
    
    /******************* Control all accordians on page load ****************************/
    
    collapseAccordians();
    $(window).resize(function(){
        collapseAccordians();
    });
    
    function collapseAccordians() {
        if ($(window).width()<768) {
            $('.collapse').collapse('hide');
        }else{
            $('.collapse').collapse('show');
        }
    }
    
    
    /*------------- Validates and Forms -------------------------------*/
    
jQuery.validator.addMethod("noSpace", function(value, element) { 
     return value.indexOf(" ") < 0 && value != ""; 
  }, "Spaces are not allowed");
    
    
    
    $('form').each(function(){
        $(this).validate();
    });
    
    
    
    
    $("#create-class-form").ajaxForm({ 
            success:       function(responseText){
                console.log(responseText);
                if (responseText.error) {
                    alert(responseText.error);
                }else if (responseText.groupID) {
                    $('#new-class').modal('hide');
                    window.location.href = "/classes/"+responseText.groupID+"/";
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    

    
    $("#join-class-form").ajaxForm({ 
            success:       function(responseText){
                var error = (responseText.error);
                if (error) {
                    alert(responseText.error);
                }else {
                    $('#join-class').modal('hide');
                    window.location.href = "/classes/"+responseText.groupID+"/";
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    
    $("#resetCode-form").ajaxForm({ 
            success:       function(responseText){
                var error = (responseText.error);
                if (error) {
                    alert(responseText.error);
                }else {
                    location.reload();
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    $(".classLockButton").click(function(){
        var element = $(this);
        var classID = element.data('options').classID;
        $.ajax({
            type: "POST",
            url: classLockURL,
            data: {groupID:classID},
            success:       function(responseText){
                var error = (responseText.error);
                if (error) {
                    alert(responseText.error);
                }else {
                    console.log(responseText.allowJoin);
                    if (responseText.allowJoin == true) {
                        //show the unlock button
                        console.log('this is false');
                        element.children().addClass('fa-unlock').removeClass('fa-lock');
                        element.addClass('btn-success').removeClass('btn-danger');
                    }else{
                        //show the lock button
                        console.log('this is true');
                        element.children().addClass('fa-lock').removeClass('fa-unlock');
                        element.addClass('btn-danger').removeClass('btn-success');
                    }
                    
                }
            },
            dataType:  'json',
            timeout:   4000
        });
    });
    
    $(".classDeleteButton").click(function(){
        var classID = $(this).data('options').classID;
        $("#checkYesNoPopup .modal-title").html('Delete?');
        $("#checkYesNoPopup .modal-body").html('Are you sure you want to delete this class?')
        $("#checkYesNoPopup").modal('show');
        $("#yesButton").unbind('click').click(function(){
            submitClassDelete(classID)
        });
    });
    
    
    function submitClassDelete(classID) {
        $.ajax({
            type: "POST",
            url: classDeleteURL,
            data: {myGroups:classID},
            success:       function(responseText){
                var error = (responseText.error);
                if (error) {
                    alert(responseText.error);
                }else {
                    location.reload();
                }
            },
            dataType:  'json',
            timeout:   4000
        });
    }
    
    
    
    $("#getCampus-form").ajaxForm({ 
            success:       function(responseText){
                var error = (responseText.error);
                if (error) {
                    alert(responseText.error);
                }else {
                    location.reload();
                }
            },
            dataType:  'json',
            timeout:   4000 
        });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
});








      function displayCode(classID, code) {
        $("#resetCode-form [name=groupID]").val(classID);
        $("#classCodeBody").html(code);
        $("#classCodePopup").modal('show');
      }
      
      
var firstTimeThrough = true;
$(function(){
  var boxes = $('[data-scroll-speed]'),
      $window = $(window);
  $window.on('scroll', function(){
    var scrollTop = $window.scrollTop();
    console.log(scrollTop);
    var run = true;
    if (scrollTop>282) {
        if (firstTimeThrough == true) {
            $(".profile-banner").css({'position':'fixed','top':'-350px'})
            $(".profile-tab").css({'position':'fixed','top':'62px'})
        }else{
            $(".profile-banner").css({'position':'fixed','top':'-280px'})
            $(".profile-tab").css({'position':'fixed','top':'110px'})
        }
        $(".profile-tab .avatar-holder").slideUp(300, function(){$(".hidden-avatar").slideDown(300);});
        
        run = false;
    }else{
        $(".profile-banner").css({'position':'absolute','top':'0px'})
        $(".profile-tab").css({'position':'absolute','top':'390px'})
        $(".hidden-avatar").slideUp(300, function(){$(".profile-tab .avatar-holder").slideDown(300);});
        firstTimeThrough = false;
        run = true;
    }
    if (run == true) {
        boxes.each(function(){
          var $this = $(this),
              scrollspeed = parseInt($this.data('scroll-speed')),
              val = - scrollTop / scrollspeed;
          $this.css('transform', 'translateY(' + val + 'px)');
        });
    }
  });
})

      
      
      
      
      
      
      
      
      