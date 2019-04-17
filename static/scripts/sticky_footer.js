var secondaryNavbar = document.getElementById('secondary-navbar');

$(window).resize(function () {
    if (secondaryNavbar === null) {
        $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + 20);
    }
    else {
        $('#sticky-footer').css('margin-bottom', parseInt($('#secondary-navbar').css("height")));
        $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + parseInt($('#secondary-navbar').css("height")) + 20);
    }
});

$(window).ready(function () {
    if (secondaryNavbar === null) {
        $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + 20);
    }
    else {
        $('#sticky-footer').css('margin-bottom', parseInt($('#secondary-navbar').css("height")));
        $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + parseInt($('#secondary-navbar').css("height")) + 20);
    }
});