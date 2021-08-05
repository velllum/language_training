
function playAllWords(task){
    var audio = document.getElementsByTagName("audio");
    var el = document.getElementById('desktopSwitch');
    var length = audio.length - 1;
    var playing = false; // текущее состояние плеера
//    var count = 0;
    var i;

    console.log(audio, task, i)

    // слушаем нажатие на кнопку
    el.addEventListener('click', function(){

        if (task == "play"){
            if (i == undefined){
                audio[0].play();
            } else {
                audio[i].play();
            }

        }

        if (task == "pause"){
            audio[i].pause();
        }

    });



//    el.addEventListener('click', playPause); // слушаем нажатие на кнопку
//
//    function playPause() {
//        if( playing) {
//            audio[0].pause();
////            el.innerText = "Paused";
//        } else {
//            audio[0].play();
////            el.innerText = "Playing..";
//        }
//        playing = !playing;
//    }

    for (let i = 0; i < length; i++) {
        audio[i].addEventListener('ended', function() {


            console.log(i, audio.length)
            audio[i + 1].play();

        });

    }
}


/* Подстановка перевода, при клике по кнопке */
$(function() {
    $('.btn-hidden').toggle();
    $("#desktopSwitch, #mobileSwitch").click(function () {
        if ($('.btn-show').is(":visible")) {
            $('.btn-show').toggle();
            $('.btn-hidden').toggle();
        } else {
            $('.btn-hidden').toggle();
            $('.btn-show').toggle();
        }
    });
});



