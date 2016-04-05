$(document).ready(function(){
    
    
        
    $.validator.addMethod("selectRequired", function(value, element, arg){
        var selectValue = $("#numberStudents option:selected").text();
        if (selectValue=="select") {
            return false;  //false means error is triggered
        }else{return true;}
     }, "You must choose.");
    
    
    $.validator.addMethod("checkSelect", function(value, element, arg){
        var selectValue = $("#numberStudents option:selected").text();
        if (selectValue=="One" && (value=="" || value==null)) {
            return false;  //false means error is triggered
        }else{return true;}
     }, "You must enter an email while selecting One student.");
        
    $('form').each(function(){
        $(this).validate();
    });
    
    
    
    $("form").ajaxForm({ 
            success:       function(responseText){
                console.log(responseText);
                if (responseText.error) {
                    alert(responseText.error);
                }else {
                    
                }
            },
            dataType:  'json',
        });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
});