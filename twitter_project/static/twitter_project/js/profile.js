$(document).ready(function(){
    
    
    $("#editProfileButton").click(function(){
        console.log("clicked");
        $(".shade").fadeIn(600);
        $(".avatar-shade").fadeIn(600);
        $(".bg-image-shade").fadeIn(600);
        $(this).fadeOut(300, function(){
            $("#editProfileCancel").fadeIn(300);
        });
    });
    $("#editProfileCancel").click(function(){
        console.log("clicked");
        $(".shade").fadeOut(600);
        $(".avatar-shade").fadeOut(600);
        $(".bg-image-shade").fadeOut(600);
        $(this).fadeOut(300, function(){
            $("#editProfileButton").fadeIn(300);
        });
    });
    
    
    
    
    var wrapper = $('<div/>').css({height:0,width:0,'overflow':'hidden'});
	$('#loadProfileImage').wrap(wrapper);
	$('#loadBGImage').wrap(wrapper);
	
	
	
	$('#avatar-shade').click(function(){
            console.log('avatar shade clicked');
	    $('#loadProfileImage').click();
	});
    
    $(".bg-image-shade").click(function(){
        console.log('avatar shade clicked');
	$('#loadBGImage').click();
    });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
});  /*-----------------------  End of document ready ------------------------*/

var imageFile,topNumberPercent,leftNumberPercent,bottomNumberPercent,rightNumberPercent;

function launchImageCrop(input) {
            if (input.files && input.files[0]) {
                if (input.files.length > 1) {
			alert('Please, only one photo.');
		}
		else{
			for (var i = 0, f; f = input.files[i]; i++) {
				ParseFile(f);
			}
		}
            }
}


	// output file information
	function ParseFile(file) {
		// display an image
		//console.log(file);
                var maxFilesize = 10048576; // 10MB
		if (file.type.indexOf("image") == 0) {
			if (file.size>maxFilesize) {alert('Only files 10MB or less please.');}
			else{
                                imageFile = file;
				var reader = new FileReader();
				reader.onload = function(e) {
                                    $('#cropDisplay').attr('src',e.target.result);
                                    $("#crop-image-popup").modal('show');
				}
				//console.log($('#upload'));
				reader.readAsDataURL(file);
				
			}
		}else{alert('Please Upload Image Files Only.');}

	}

var ias;
function activateCrop() {
    
			var imageWidth = $('#cropDisplay').width();
			var imageHeight = $('#cropDisplay').height();
                        
			ias = $('#cropDisplay').imgAreaSelect({
                                fadeSpeed: 1000,
                                persistent: true,
				aspectRatio: '4:4',
				handles: true,
				x1: 0, y1: 0, x2: 10, y2: 10,
				minWidth: 10,
				minHeight: 10,
				onSelectEnd:function(img, selection) {
					console.log('Current width: '+imageWidth+' and height: '+imageHeight);
					topNumberPercent = selection.y1/imageHeight;
					leftNumberPercent = selection.x1/imageWidth;
					bottomNumberPercent = selection.y2/imageHeight;
					rightNumberPercent = selection.x2/imageWidth;
					
                                        console.log("Top: "+topNumberPercent);
                                        console.log("left: "+leftNumberPercent);
                                        console.log("bottom: "+bottomNumberPercent);
                                        console.log("right: "+rightNumberPercent);
                                        
                                        console.log();
                                        $('#crop-image-popup button').removeClass('disabled');
				},
				instance: true,
			});
			
			if (imageWidth>=imageHeight) {
				var first = parseInt(imageHeight*.2);
				var second = parseInt(imageHeight*.6);
			}else{
				var first = parseInt(imageWidth*.2);
				var second = parseInt(imageWidth*.6);
			}
			
			ias.setSelection(first, first, second, second, true);
			ias.setOptions({ show: true });
			ias.update();
			
}



$("#crop-image-popup").on('shown.bs.modal', function() { 
    setTimeout( "activateCrop();",1000 );
});
//FOR HIDDING
$("#crop-image-popup").on('hidden.bs.modal', function() {
    ias.setOptions({ fadeSpeed: 0 });
    ias.update();
    ias.cancelSelection();
});



    $('#crop-image-popup button').click(function(){
            formData= new FormData();
            formData.append("image", imageFile);
            formData.append("topPercent", topNumberPercent);
            formData.append("leftPercent", leftNumberPercent);
            formData.append("bottomPercent",bottomNumberPercent);
            formData.append("rightPercent",rightNumberPercent);
            
            $.ajax({
                type: "POST",
                url: sendFileURL,
                data: formData,
                success:       function(responseText){
                    var error = (responseText.error);
                    if (error) {
                        alert(responseText.error);
                    }else {
                        console.log(responseText);
                        location.reload();
                    }
                },
                dataType:  'json',
                processData: false,
                contentType: false,
                timeout:   6000
            });
    });
    
    





//----------------- Background Header Image upload -------------------------------



function launchBGCrop(input) {
            if (input.files && input.files[0]) {
                if (input.files.length > 1) {
			alert('Please, only one photo.');
		}
		else{
			for (var i = 0, f; f = input.files[i]; i++) {
				ParseFile30(f);
			}
		}
            }
}


	// output file information
	function ParseFile30(file) {
		// display an image
		//console.log(file);
                var maxFilesize = 30048576; // 30MB
		if (file.type.indexOf("image") == 0) {
			if (file.size>maxFilesize) {alert('Only files 10MB or less please.');}
			else{
                                imageFile = file;
				var reader = new FileReader();
				reader.onload = function(e) {
                                    $('#bgCropDisplay').attr('src',e.target.result);
                                    $("#crop-bg-image-popup").modal('show');
				}
				//console.log($('#upload'));
				reader.readAsDataURL(file);
				
			}
		}else{alert('Please Upload Image Files Only.');}

	}

var ias;
function activateBGCrop() {
    
			var imageWidth = $('#bgCropDisplay').width();
			var imageHeight = $('#bgCropDisplay').height();
                        
			ias = $('#bgCropDisplay').imgAreaSelect({
                                fadeSpeed: 1000,
                                persistent: true,
				aspectRatio: '3:1',
				handles: true,
				x1: 0, y1: 0, x2: 10, y2: 10,
				minWidth: 10,
				minHeight: 10,
				onSelectEnd:function(img, selection) {
					console.log('Current width: '+imageWidth+' and height: '+imageHeight);
					topNumberPercent = selection.y1/imageHeight;
					leftNumberPercent = selection.x1/imageWidth;
					bottomNumberPercent = selection.y2/imageHeight;
					rightNumberPercent = selection.x2/imageWidth;
					
                                        console.log("Top: "+selection.y1);
                                        console.log("left: "+selection.x1);
                                        console.log("bottom: "+selection.y2);
                                        console.log("right: "+selection.x2);
                                        
                                        console.log();
                                        $('#crop-bg-image-popup button').removeClass('disabled');
				},
				instance: true,
			});
			
			if (imageWidth>=imageHeight) {
				var first = parseInt(imageHeight*.11);
				var x2 = parseInt(imageHeight*.94);
                                var y2 = parseInt(imageHeight*.39);
			}else{
				var first = parseInt(imageWidth*.06);
				var x2 = parseInt(imageHeight*.53);
                                var y2 = parseInt(imageHeight*.22);
			}
			
			ias.setSelection(first, first, x2, y2, true);
			ias.setOptions({ show: true });
			ias.update();
			
}



$("#crop-bg-image-popup").on('shown.bs.modal', function() { 
    setTimeout( "activateBGCrop();",1000 );
});
//FOR HIDDING
$("#crop-bg-image-popup").on('hidden.bs.modal', function() {
    ias.setOptions({ fadeSpeed: 0 });
    ias.update();
    ias.cancelSelection();
});



    $('#crop-bg-image-popup button').click(function(){
            formData= new FormData();
            formData.append("image", imageFile);
            formData.append("topPercent", topNumberPercent);
            formData.append("leftPercent", leftNumberPercent);
            formData.append("bottomPercent",bottomNumberPercent);
            formData.append("rightPercent",rightNumberPercent);
            
            $.ajax({
                type: "POST",
                url: sendBGImageFileURL,
                data: formData,
                success:       function(responseText){
                    var error = (responseText.error);
                    if (error) {
                        alert(responseText.error);
                    }else {
                        console.log(responseText);
                        location.reload();
                    }
                },
                dataType:  'json',
                processData: false,
                contentType: false,
                timeout:   6000
            });
    });
    
    







