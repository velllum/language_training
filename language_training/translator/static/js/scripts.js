
$('.btn-hidden').toggle();

var audio = document.getElementsByClassName("audio");
var array = []

for (let a of audio) {
    array.push(a.getAttribute('src'))
}
var count = 0;
var length = array.length-1;

$(".my_audio").trigger('load');
$('.my_audio').append("<source id='sound_src' src=" + array[0] + " type='audio/mpeg'>");

function stop_audio(){
    $("#sound_src").attr("src", array[0]);
    $(".my_audio").trigger('load');
    $(".my_audio").trigger('pause');
    $(".my_audio").prop("currentTime",0);
    count = 0;
 }

function hidden() {
    $('.btn-hidden').toggle();
    $('.btn-show').toggle();
 }

function show() {
    $('.btn-show').toggle();
    $('.btn-hidden').toggle();
 }

function play_audio(task) {
    if(task == 'play'){
        $(".my_audio").trigger('play');
        hidden()
    }
    if(task == 'stop'){
        stop_audio()
        show()
    }
 }

$('.my_audio').on('ended', function() {
    if (count == length) {
        stop_audio()
        show()
    } else {
        count++;
        $("#sound_src").attr("src", array[count]);
        $(".my_audio").trigger('load');
        play_audio('play');
        hidden()
    }

});












