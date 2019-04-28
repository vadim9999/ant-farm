var item = "cursorQ dropdown-item";
var resolution = "640x480";

function onQ720() {
    console.log("in function___720______");
    resolution = "1024x768"
    document.getElementById("Q720").setAttribute("class", item + " active")
    document.getElementById("Q480").setAttribute("class", item)
    document.getElementById("Q240").setAttribute("class", item)
    document.getElementById("Q240").setAttribute("disabled", "true")
    // document.getElementById('info').removeAttribute("title")
    // $('#videoResolution').prop('disabled', true);
    // document.getElementById("info").removeAttribute("style")
    // $('#info').tooltip('enable')
}



function onQ480() {
    resolution = "640x480"
    document.getElementById("Q720").setAttribute("class", item)
    document.getElementById("Q480").setAttribute("class", item + " active")
    document.getElementById("Q240").setAttribute("class", item)
}

function onQ240() {
    resolution = "320x240"
    document.getElementById("Q720").setAttribute("class", item)
    document.getElementById("Q480").setAttribute("class", item)
    document.getElementById("Q240").setAttribute("class", item + " active")
}

function startPreview() {
    userId = getUrlParam('id', 'Empty')
    enableButtonStop('preview')
    document.getElementById("start-record").removeAttribute("disabled")
    document.getElementById("capture-image").removeAttribute("disabled")
  
    var xhttp = new XMLHttpRequest();
    streamUrl = location.protocol + "//" + location.host + "/stream.mjpg?id=" + userId;
    console.log(streamUrl);
  
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
  
        console.log("POST /start _____");
        console.log(this.responseText);
        document.getElementById('badge').src = streamUrl;
      }
    }
    xhttp.open("POST", "/start?id=" + userId, true);
    xhttp.send(resolution);
  
  }