
/* Подстановка перевода, при клике по кнопке */
$(function() {
    $('.hidden').toggle();
    $("#desktopSwitch, #mobileSwitch").click(function () {
        if ($('.show').is(":visible")) {
            $('.show').toggle();
            $('.hidden').toggle();
        } else {
            $('.hidden').toggle();
            $('.show').toggle();
        }
    });
});

