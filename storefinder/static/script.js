

$(document).ready(function() {
    $('.datepicker').datepicker({
        maxDate: new Date()
    });
    $('select').formSelect();
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();

});

function openNew() {
    setTimeout(function(){ window.location.href = "/new"; }, 200);
}



