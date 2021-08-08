

//var tagAudio = document.getElementsByTagName("audio");
//var arrayAudio = []
//
//for (let a of tagAudio) {
//    arrayAudio.push(a.getAttribute('src'))
//}
//
//console.log(arrayAudio);
//
//function playAllWords(task) {
//
//    var audio = new Audio();
//
//    if (task === "play") {
//
//        var current = 0;
//        audio.src = arrayAudio[0];
//        audio.autoplay = true;
//
//        audio.onended = function() {
//            if (current >= arrayAudio.length) {
//                console.log("stop")
//                this.stop();
//            } else if (task === "play") {
//                console.log("play")
//                current++;
//                this.src = arrayAudio[current];
//                this.play();
//            }
//        }
//    }
//
//    Audio.prototype.stop = function() {
//        console.log("Audio.prototype.stop")
//        this.pause();
//        this.currentTime = 0;
//    }
//
//    if (task === "pause") {
//        console.log("stop")
//        this.stop();
//    }
//}



//var tagAudio = document.getElementsByTagName("audio");
//var arrayAudio = []
//
//for (let a of tagAudio) {
//    arrayAudio.push(a.getAttribute('src'))
//}
//
//console.log(arrayAudio);
//
//function playAllWords(task){
////    var audio = new Audio();
//    var length = arrayAudio.length;
//
////    console.log(audio, task)
//    var audio = new Audio();
//
//    audio.src = arrayAudio[0];
//    audio.autoplay = true;
//    audio.preload = "auto";
//
//    for (let i = 0; i < length; i++) {
//        audio.src = arrayAudio[i];
//        audio.play();
//        audio.addEventListener('ended', function() {
//
//            audio.play();
//
//        }, false);
//    }
//
//
//    Audio.prototype.stop = function() {
//        console.log("Audio.prototype.stop")
//        this.pause();
//        this.currentTime = 0;
//    }
//}




//var tagAudio = document.getElementsByTagName("audio");
//var array = []
//
//for (let a of tagAudio) {
//    array.push(a.getAttribute('src'))
//}
//
//var el = document.getElementById('player');
//var playing = false; // текущее состояние плеера
//
//var player = new Audio();
//
////function playAllWords(task){
//for (let i = 0; i < array.length; i++) {
//    player.src = array[i]
//    player.preload = "auto";
//
//
//player.addEventListener('ended', function(){ // слушаем окончание трека
////    el.innerText = "Done";
//    console.log("до", playing)
//    playing = false;
//    console.log("после", playing)
//});
//}
//el.addEventListener('click', function(){
//
////    for (let i = 0; i < arrayAudio.length; i++) {
//
//            player.preload = "auto";
//            console.log("player.ended", player.ended)
//    //        player.load();
//            if(playing){
//                player.pause();
//            //        el.innerText = "Paused";
//            } else {
//
//    //            player.cloneNode(true).play();
//            player.play();
//            //        el.innerText = "Playing..";
//            }
//
//    //    }
//        playing = !playing;
//        console.log("playing = !playing;", playing)
//
//
////    }
//}); // слушаем нажатие на кнопку
//
//
///* Подстановка перевода, при клике по кнопке */
//$(function() {
//    $('.btn-hidden').toggle();
//    $("#desktopSwitch, #mobileSwitch").click(function () {
//        if ($('.btn-show').is(":visible")) {
//            $('.btn-show').toggle();
//            $('.btn-hidden').toggle();
//        } else {
//            $('.btn-hidden').toggle();
//            $('.btn-show').toggle();
//        }
//    });
//});





//var audio = document.getElementsByTagName("audio");
//var array = []
//
//for (let a of audio) {
//    array.push(a.getAttribute('src'))
//}
//
//iBtn=document.getElementsByTagName('button');
//
//
//for(j = 0; j < audio.length; j++)
//{
//    audio[j].addEventListener
//    (
//        'click',
//        function()
//        {
////            var audio=new Audio(this.id+'.mp3');
//
//            if(audio[j].paused)
//            {
//                audio[j].play();
////                iBtn[j].classList.remove("play");
////                iBtn[j].classList.add("pause");
//            }
//            else
//            {
//                audio[j].pause();
////                iBtn[j].classList.remove("pause");
////                iBtn[j].classList.add("play");
//            }
//
//        },false
//    );
//}




function onlyPlayOneIn(container) {
  container.addEventListener("play", function(event) {
  audio_elements = container.getElementsByTagName("audio")
    for(i=0; i < audio_elements.length; i++) {
      audio_element = audio_elements[i];
      if (audio_element !== event.target) {
        audio_element.pause();
      }
    }
  }, true);
}

document.addEventListener("DOMContentLoaded", function() {
  onlyPlayOneIn(document.body);
});



