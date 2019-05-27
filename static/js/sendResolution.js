var item = "cursorQ dropdown-item";
var resolution = "854x480";


function onQ720() {
  resolution = "1280x720"
  document.getElementById("Q720").setAttribute("class", item + " active")
  document.getElementById("Q480").setAttribute("class", item)
  document.getElementById("Q240").setAttribute("class", item)
  onChangeQuality()
}

function onQ480() {
  resolution = "854x480"
  document.getElementById("Q720").setAttribute("class", item)
  document.getElementById("Q480").setAttribute("class", item + " active")
  document.getElementById("Q240").setAttribute("class", item)
  onChangeQuality()
}

function onQ240() {
  resolution = "426x240"
  document.getElementById("Q720").setAttribute("class", item)
  document.getElementById("Q480").setAttribute("class", item)
  document.getElementById("Q240").setAttribute("class", item + " active")
  onChangeQuality()
}

function onChangeQuality() {
  if (isPreviewStart) {
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
  if (document.getElementById("start-stream").hasAttribute("disabled") !== true) {
    document.getElementById("start-record").removeAttribute("disabled")
    document.getElementById("capture-image").removeAttribute("disabled")
  }


  var xhttp = new XMLHttpRequest();
  streamUrl = location.protocol + "//" + location.host + "/stream.mjpg?id=" + userId;

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
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
  isBlocked = false
  document.getElementById("capture-image").disabled = true;
  document.getElementById("start-record").disabled = true;
  var xhttp = new XMLHttpRequest();

  xhttp.open("GET", "/stop?id=" + userId, true);
  xhttp.send();
}

// ----------stream-------------
function startStream() {
  userId = getUrlParam('id', 'Empty')

  var xhttp = new XMLHttpRequest();
  var userId = getUrlParam('id', 'Empty')

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var str = this.responseText;
      
      var data = JSON.parse(str)
      if (data["youtube"].length > 0 && data["key"].length > 0) {
        startBlinking("blinkingStream")
        enableButtonStop("stream")
        
        var e = document.getElementById("resolutionStream")
        let resolution = e.options[e.selectedIndex].value;

        var xhttp2 = new XMLHttpRequest();

        xhttp2.open("POST", "/start_stream?id=" + userId, true);
        xhttp2.send(getResolution(resolution));
        waitStartPreview()
      }else{
        alert("Введіть 'Посилання' та 'Ключ' в Налаштуваннях ")
      }

    }
  }
  xhttp.open("GET", "/stream_settings?id=" + userId, true);
  xhttp.send();


}

function stopStream() {
  userId = getUrlParam('id', 'Empty')
  stopBlinking("blinkingStream")
  enableButtonStart("stream")
  enableButtonStart("preview")
  isPreviewStart = false
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/stop_stream?id=" + userId, true);
  xhttp.send();

}

function waitStartPreview() {
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        startPreview()
        document.getElementById("capture-image").disabled = true;
        document.getElementById("start-record").disabled = true;
      }
    }
  xhttp.open("GET", "/wait_start_preview?id=" + userId, true);
  xhttp.send();
}
