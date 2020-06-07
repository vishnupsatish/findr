

$(document).ready(function() {
    $('.datepicker').datepicker({
        maxDate: new Date()
    });
    $('select').formSelect();
    $('.sidenav').sidenav();
    if($(window).width() > 750) {
        $('.card-class').addClass('s4');
        $('.card-class').removeClass('s6');
        $('.card-class').removeClass('s12');
    }else if ($(window).width() < 750 && $(window).width() > 650){
        $('.card-class').addClass('s6');
        $('.card-class').removeClass('s4');
        $('.card-class').removeClass('s12');
    }
    else {
        $('.card-class').addClass('s12');
        $('.card-class').removeClass('s6');
        $('.card-class').removeClass('s4');
    }
    


    if($(window).width() > 600) {
        $('#search-button').css("top", "15px")
    }
    if($(window).width() <= 600) {
        $('#search-button').css("top", "10px")

    }

});

$(window).on('resize', function() {
    if($(window).width() > 750) {
        $('.card-class').addClass('s4');
        $('.card-class').removeClass('s6');
        $('.card-class').removeClass('s12');
    }else if ($(window).width() < 750 && $(window).width() > 650){
        $('.card-class').addClass('s6');
        $('.card-class').removeClass('s4');
        $('.card-class').removeClass('s12');
    }
    else {
        $('.card-class').addClass('s12');
        $('.card-class').removeClass('s6');
        $('.card-class').removeClass('s4');
    }

    if($(window).width() > 600) {
        $('#search-button').css("top", "15px")
    }
    if($(window).width() <= 600) {
        $('#search-button').css("top", "10px")

    }
    var new_search_width = String($(window).width()/100 + 86) + "%"
    new_search_width = String($(window).width()/100 + $(window).width()/14) + "%"

    console.log(new_search_width)
    //$('.input-field').css("width", new_search_width)

    
})




