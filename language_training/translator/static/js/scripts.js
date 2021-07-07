
/* Подстановка перевода, при клике по кнопке */
$(function() {
    $('.hidden').toggle();
    $("#textSwitch").click(function () {
        if ($('.show').is(":visible")) {
            $('.show').toggle();
            $('.hidden').toggle();
        } else {
            $('.hidden').toggle();
            $('.show').toggle();
        }
    });
});

