//$(function() {
//    var btn = $("[id='#textSwitch']");
//    var text_hidden = $("[class='visually-hidden']")
//    var text_display = $("[class='visually']")
//    var toggled = false;
//
//    btn.on("click", function() {
//        if(!toggled)
//        {
//          toggled = true;
//          $("[class='visually-hidden']").toggleClass('sually');
//          $("[class='sually']").toggleClass('visually-hidden');
//        } else {
//          toggled = false;
//          $("[class='sually']").toggleClass('visually-hidden');
//          $("[class='visually-hidden']").toggleClass('sually');
//        }
//    });
//});

$("[id='#textSwitch']").click(function () {
    $('.visually-hidden').toggle();

    if ($('.sually').is(":visible")) { // !!!
        $('.sually').hide();
        $('.visually-hidden').show();
    } else {
        $('.visually-hidden').hide();
        $('.sually').show();
    }
});