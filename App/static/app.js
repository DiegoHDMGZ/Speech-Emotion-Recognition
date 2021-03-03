// Start record 
let start = document.getElementById('btnStart');   
// Stop record 
let stop = document.getElementById('btnStop'); 
// 2nd audio tag for play the audio 
let playAudio = document.getElementById('adioPlay');

start.disabled = false;
stop.disabled = true;
playAudio.disabled = true;

const txtLabel =  document.querySelector('#txtLabel');
function setLabel(label) {
	txtLabel.textContent = label;
}


async function capture(){
    // allow use camera in browser
    const mediaStreamVideo = await navigator.mediaDevices.getUserMedia({audio: true});

    // activate cameta in browser
    var canvas = document.querySelector("audio");
    if ('srcObject' in canvas) {
        canvas.srcObject = mediaStreamVideo;
    } else { // Avoid using this in new browsers, as it is going away.
        canvas.src = URL.createObjectURL(mediaStreamVideo);
    }

    // Optional frames per second argument.
    var stream = canvas.captureStream(25);
    var dataArray = [];
    //var options = { mimeType: "video/wab; codecs=vp9" };
    mediaRecorder = new MediaRecorder(stream);

    // Start event 
    start.addEventListener('click', function (ev) {
        start.disabled = true;
        stop.disabled = false;
        playAudio.disabled = true;
        mediaRecorder.start(); // console.log(mediaRecorder.state); 
    }) 
    // Stop event 
    stop.addEventListener('click', function (ev) {
        start.disabled = false;
        stop.disabled = true;
        playAudio.disabled = false;
        mediaRecorder.stop(); // console.log(mediaRecorder.state); 
    }) 
    // If audio data available then push it to the chunk array 
    mediaRecorder.ondataavailable = function (ev) { 
        dataArray.push(ev.data);
    } 

    mediaRecorder.onstop = function (ev) {   
        // blob of type mp3 
        let audioData = new Blob(dataArray, { 'type': 'audio/mp3;' });
        console.log(audioData);
		setLabel('Cargando predicción...')
        var reader = new FileReader();
        reader.readAsDataURL(audioData); 
        reader.onloadend = function() {
            base64 = reader.result;
            base64 = base64.split(',')[1];
            //fetch('/audio_update', {method: 'POST', body: base64});
            fetch('/audio_update', {method: 'POST', body: base64}).then(res => res.json()).then(({result}) => {
				console.log(result);
				setLabel(result)
			  });
            //console.log(base64);
        }
           
        // After fill up the chunk array make it empty 
        dataArray = []; 

        // Creating audio url with reference of created blob named 'audioData' 
        let audioSrc = window.URL.createObjectURL(audioData); 
        
        // Pass the audio url to the 2nd video tag 
        playAudio.src = audioSrc;
    } 
}
capture();
