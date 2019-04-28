var item = "cursorQ dropdown-item";
var resolution = "640x480";
var isPreviewStart = false;

function onQ720() {
    
    console.log("in function___720______");
    resolution = "1024x768"
    document.getElementById("Q720").setAttribute("class", item + " active")
    document.getElementById("Q480").setAttribute("class", item)
    document.getElementById("Q240").setAttribute("class", item)
    onChangeQuality()
    // document.getElementById("Q240").setAttribute("disabled", "true")
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
    onChangeQuality()
}

function onQ240() {
    resolution = "320x240"
    document.getElementById("Q720").setAttribute("class", item)
    document.getElementById("Q480").setAttribute("class", item)
    document.getElementById("Q240").setAttribute("class", item + " active")
    onChangeQuality()
}

function onChangeQuality(){
  if (isPreviewStart){
    stopPreview()
    setTimeout(function () {
      startPreview()
    }
      , 1000);
    
  }
}

function startPreview() {
    userId = getUrlParam('id', 'Empty')
    isPreviewStart = true
    
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

  function stopPreview() {
    userId = getUrlParam('id', 'Empty')
    enableButtonStart("preview")
    isPreviewStart = false
    document.getElementById("capture-image").disabled = true;
    document.getElementById("start-record").disabled = true;
    var xhttp = new XMLHttpRequest();
  
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
        console.log("GET");
        console.log(this.responseText);
      }
    }
    xhttp.open("GET", "/stop?id=" + userId, true);
    xhttp.send();
  }