var tagAudio = document.getElementsByTagName("audio");
var arrayAudio = []
var host = window.location.origin;


for (let a of tagAudio) {
    arrayAudio.push(a.getAttribute('src'))
}

console.log(arrayAudio, host, host.concat(arrayAudio[0]));

//$('input').click(function() {
//  audio.src = this.name
//  audio.play();
//})
function playAllWords(task){
    var audio = new Audio();
    var current = 0;
    audio.src = host.concat(arrayAudio[0]);
    //player.autoplay = true;
    console.log(audio.src)
    audio.play();
}
//player.onended = function() {
//  current++;
//  if (current >= arrayAudio.length) current = 0;
//  player.src = arrayAudio[current];
//  player.play();
//}


//function playAllWords(task){
//    var audio = document.getElementsByTagName("audio").textContent;
//    console.log(audio)
//    var el = document.getElementById('desktopSwitch');
//    var length = audio.length - 1;
//    var playing = false; // текущее состояние плеера
////    var count = 0;
//
//    console.log(audio, task)
//
//    var array = []
//    for (let i = 0; i < length; i++) {
//
//
//
//    }
//
//    for (let i = 0; i < length; i++) {
//        audio[i].addEventListener('ended', function() {
//
//
//            el.addEventListener('click', function(){
//
//                if (task == "play"){
//                    if (i == undefined){
//                        audio[0].play();
//                    } else {
//                        audio[i].play();
//                    }
//
//                }
//
//                if (task == "pause"){
//                    audio[i].pause();
//                }
//
//            });
//
//
//            console.log(i, audio.length)
//            audio[i + 1].play();
//
//        });
//
//    }
//}


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



