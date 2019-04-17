$(window).resize(function () {
    $('#sticky-footer').css('margin-bottom', parseInt($('#secondary-navbar').css("height")));
    $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + parseInt($('#secondary-navbar').css("height")) + 20);
});

$(window).ready(function () {
    $('#sticky-footer').css('margin-bottom', parseInt($('#secondary-navbar').css("height")));
    $('body').css('margin-bottom', parseInt($('#sticky-footer').css("height")) + parseInt($('#secondary-navbar').css("height")) + 20);
});