$(document).ready(function(){
    $(window).scroll(function(){
        if($(this).scrollTop()>10)
            {
                $(".nav").addClass("nav-fixed");
                
            }
        else{
                $(".nav").removeClass("nav-fixed");
               
        }
    });
    
});