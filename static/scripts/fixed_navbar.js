$(function () {
    var lastScrollTop = 0;
    var $navbar = $('#main-navbar');

    $(window).scroll(function (event) {
        var st = $(this).scrollTop();

        if (st > lastScrollTop) { // scroll down

            // use this is jQuery full is used
            $navbar.fadeOut()

            // use this to use CSS3 animation
            // $navbar.addClass("fade-out");
            // $navbar.removeClass("fade-in");

            // use this if no effect is required
            // $navbar.hide();
        } else { // scroll up

            // use this is jQuery full is used
            $navbar.fadeIn()

            // use this to use CSS3 animation
            // $navbar.addClass("fade-in");
            // $navbar.removeClass("fade-out");

            // use this if no effect is required
            // $navbar.show();
        }
        lastScrollTop = st;
    });
});

$(window).resize(function () {
    $('body').css('padding-top', parseInt($('#main-navbar').css("height")) + 10);
});

$(window).ready(function () {
    $('body').css('padding-top', parseInt($('#main-navbar').css("height")) + 10);
});