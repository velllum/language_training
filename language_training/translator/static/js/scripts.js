function playAllWords(){
    var audio = document.getElementsByTagName("audio");
//    var object = new Audio()
    console.log(audio, audio.length);
//    console.log(object);


    for (let i = 0; i < audio.length; i++){

        console.log(audio[i], audio[i].currentSrc);

        audio[i].addEventListener("ended", function(){

            console.log(audio[i]);
            var object = new Audio(audio[i+1].currentSrc)
//            object.src = audio[i].currentSrc;
            object.play();

        });

    }
//    audio[0].play();
//    for (let i = 0; i < audio.length; i++) {
//      object.addEventListener('canplaythrough ended', function() {
//
//          console.log(i, audio[i].currentSrc, audio[i].duration);
////          audio[i + 1].play();
//          object.src = audio[i].currentSrc;
//          object.play();
//
//      });
//    }
}



