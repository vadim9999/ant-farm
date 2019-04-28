// document.getElementById("TextBlock").innerHTML = 100;


loadDoc();
window.setInterval(function () {
  //  loadDoc()
}, 5000)

// ***********************Socket*****************
// console.log("Executing")
// var socket = new WebSocket('ws://' + window.location.hostname + ':8084/');
//
// socket.onopen = function(){
// console.log('Connection is set')
// socket.send("Hi I am from client")
// }

//console.log(socket)
// socket.onmessage = function(event){
// console.log(event.data)
// }

// socket.onclose = function(event) {
// if(event.wasClean){
// console.log('Connection was Closed')
// }
// else{
// console.log("connection was killed")
// }
// console.log('Code ' + event.code + ' reason '+ event.reason)
// }
// *********************************************
var h1 = document.getElementById('stopWatch'),
  start = document.getElementById('start'),
  stop = document.getElementById('stop'),
  clear = document.getElementById('clear'),
  seconds = 0, minutes = 0, hours = 0,
  t;

function add() {
  seconds++;
  if (seconds >= 60) {
    seconds = 0;
    minutes++;
    if (minutes >= 60) {
      minutes = 0;
      hours++;
    }
  }

  h1.innerHTML = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);

  timer();
}
function timer() {
  t = setTimeout(add, 1000);
}
// timer();
function onFullScreen() {
  var fullScreen = document.getElementById("fullScreen");
  console.log(fullScreen.webkitRequestFullscreen);
  fullScreen.webkitRequestFullScreen()
  if (document.webkitFullscreenElement) {
    document.webkitCancelFullScreen();
    var image = document.getElementById("badge");
    // image.style = "width:640; height:480"
    image.setAttribute("width", "640")
    image.setAttribute("height", "480")
    // image.width="640";
    // image.height = "480";
  }

  else {
    fullScreen.webkitRequestFullScreen();
    var image = document.getElementById("badge");
    // image.style = "width:100%; height:100%"
    image.setAttribute("width", "100%")
    image.setAttribute("height", "100%")

  };

  //  fullScreen.webkitRequestFullScreen()
}
function startStopWatch() {
  h1.innerHTML = "00:00:00";
  seconds = 0; minutes = 0; hours = 0;
  timer();
}

function stopStopWatch(id) {

  clearTimeout(t);
}
function startBlinking(id) {
  document.getElementById(id).style.backgroundColor = "red";
  document.getElementById(id).style.animation = "blinker 1.5s cubic-bezier(.5, 0, 1, 1) infinite alternate"
}

function stopBlinking(id) {
  document.getElementById(id).style.backgroundColor = "";
  document.getElementById(id).style.animation = ""
}

function enableButtonStop(id) {
  document.getElementById("stop-" + id).removeAttribute("disabled")
  document.getElementById("start-" + id).disabled = "true"
}

function enableButtonStart(id) {
  document.getElementById("start-" + id).removeAttribute("disabled")
  document.getElementById("stop-" + id).disabled = "true"
}
/* Start button */
// start.onclick = timer;

/* Stop button */
// stop.onclick = function() {

// }

/* Clear button */
// clear.onclick = function() {
//     h1.innerHTML = "00:00:00";
//     seconds = 0; minutes = 0; hours = 0;
// }


function loadDoc() {

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      // var data = document.test_form.test_text.value;
      sensors = JSON.parse(this.responseText)
      // console.log(data);
      // document.getElementById("TextBlock").innerHTML = this.responseText ;
      document.getElementById("sotTemp").innerHTML = sensors[0][0];
      document.getElementById("sotHum").innerHTML = sensors[0][1] + "%";
      document.getElementById("humidityCircle").setAttribute("stroke-dasharray", (sensors[0][1] + " 135"));
      let sotHum = sensors[0][1];
      // document.getElementById("humAnimation").setAttribute("values",
      // ("0 200; " + ((sotHum/6) + " 180; ") + ((sotHum/4) + " 150; ") + ((sotHum/7) + " 135; ") + (sensors[0][1] + " 135; ")+(sensors[0][1] + " 135; ")));

      document.getElementById("arenaTemp").innerHTML = sensors[1][0];
      document.getElementById("arenaHum").innerHTML = sensors[1][1];
      document.getElementById("roomTemp").innerHTML = sensors[2][0];
      document.getElementById("roomHum").innerHTML = sensors[2][1];
      // Water level
      switch (sensors[3]) {
        case 1:
          document.getElementById("waterLvlLow").innerHTML = 1;
          document.getElementById('topWater').style.background = "red";
          document.getElementById('sky').style.height = '80%';
          break;
        case 2:
          document.getElementById("waterLvlMiddle").innerHTML = 1;
          document.getElementById('topWater').style.background = "orange";
          document.getElementById('sky').style.height = '50%';
          break;
        case 3:
          document.getElementById("waterLvlHigh").innerHTML = 1;
          document.getElementById('topWater').style.background = "green";
          document.getElementById('sky').style.height = '20%';
          break;
      }
      console.log("Response");
      console.log(JSON.parse(this.responseText));
    }
  }
  xhttp.open("GET", "/sensors", true);
  xhttp.send();
}

function test() {
  console.log("_____test______");
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
      console.log("TEST");
      // console.log(this.responseText);
    }
  }
  xhttp.open("GET", "/test?id=" + userId, true);
  xhttp.send();
}
// --------------video files

// function onDeleteFile(){
//   console.log("inFunctiononDeleteFile")
// }
function onRefreshList() {
  console.log("inFunction")
  setTimeout(function () {
    getVideoFiles();
  }
    , 2000);
}

function getExtensionFile(filename) {
  return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
}

function getVideoFiles() {
  console.log("Call this function__________");

  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log("get video files");
      var response = this.responseText;
      var data = response.substring(2, response.length - 2)
      var fileNames = data.split("', '");
      console.log("fileNames");
      console.log(fileNames)

      console.log(data)
      document.getElementById("fileList").innerHTML = "";



      if (fileNames != undefined && fileNames.length > 0 && fileNames[0] != "") {
        fileNames.forEach(file => {
          var a = document.createElement('a');
          a.className = "list-group-item list-group-item-action";
          a.innerHTML = file;
          // a.href = "/" + video;
          // console.log(a);
          console.log(getExtensionFile(file));
          var mediaIcon = document.createElement("i");

          if (getExtensionFile(file) == "h264") {
            mediaIcon.className = "videoIcon fas fa-film"
          } else if (getExtensionFile(file) == "jpg") {
            mediaIcon.className = "videoIcon fas fa-image"
          }



          var trash = document.createElement("i");
          trash.className = "glyphicon fas fa-trash-alt"
          trash.setAttribute("onclick", "onRefreshList()")

          var trashHref = document.createElement("a")
          trashHref.href = "/delete/" + file
          // trashHref.setAttribute("id", "refreshFiles")
          trashHref.appendChild(trash);

          var downloadHref = document.createElement("a");
          downloadHref.href = "/download/" + file;

          var download = document.createElement("i");
          download.className = "glyphicon fas fa-download"
          downloadHref.appendChild(download)


          a.appendChild(downloadHref)
          a.appendChild(trashHref)
          a.appendChild(mediaIcon);
          document.getElementById("fileList").appendChild(a);

        });
      }

      // var a = document.createElement('a');
      // a.className = "list-group-item list-group-item-action";
      // a.innerHTML = "OKOK";
      // console.log(a);
      // document.getElementById("fileList").innerHTML = "";
      // document.getElementById("fileList").appendChild(a);
      // var videoFiles = JSON.parse(this.responseText)
      // console.log(videoFiles)
      console.log(this.responseText);
    }
  }
  xhttp.open("GET", "/media?id=" + userId, true);
  xhttp.send();
}

function buildFiles() {
  // <a href="#" class="list-group-item list-group-item-action">Dapibus ac facilisis in</a>
  var a = document.createElement('a');
  a.className = "list-group-item list-group-item-action";
  a.innerHTML = "OKOK";
  console.log(a);
  document.getElementById("fileList").innerHTML = "";
  document.getElementById("fileList").appendChild(a);
}
// ----------------------------------------
function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
    vars[key] = value;
  });
  return vars;
}

function getUrlParam(parameter, defaultvalue) {
  var urlparameter = defaultvalue;
  if (window.location.href.indexOf(parameter) > -1) {
    urlparameter = getUrlVars()[parameter];
  }
  return urlparameter;
}

// -------preview---------

function captureImage() {
  userId = getUrlParam('id', 'Empty')
  // enableButtonStart("preview")
  var xhttp = new XMLHttpRequest();
  var filename = document.getElementById("capture-input").value;

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
      console.log("GET");
      var a = document.createElement('div');
      a.className = "alerts alert alert-success alert-dismissible fade show";
      a.setAttribute("role", "alert")
      a.innerHTML = "Зображення створено успішно!"

      var button = document.createElement('button');
      button.className = "close";
      button.type = "button"
      button.setAttribute("data-dismiss", "alert")
      button.setAttribute("aria-label", "Close")
      a.appendChild(button)

      var span = document.createElement("span");
      span.setAttribute("aria-hidden", "true")
      span.innerHTML = "&times;"
      button.appendChild(span)

      document.getElementById("alertBlock").innerHTML = ""
      document.getElementById("alertBlock").appendChild(a)
      // document.getElementById("alertBlock").innerHTML = ""

      setTimeout(function () {
        document.getElementById("alertBlock").innerHTML = "";
      }, 5000);
      console.log(this.responseText);
    }
  }
  xhttp.open("POST", "/capture_image?id=" + userId, true);
  xhttp.send(filename);
}





// -------------------
function getResolution(resolution){
  switch (resolution) {
    case "720":
      return "1024x768"
      break;

    case "480":
      return "640x480"
      break;

    case "240":
      return "320x240"
      break;
    default:
      break;
  }
}
// ----------stream-------------
function startStream() {
  userId = getUrlParam('id', 'Empty')
  startBlinking("blinkingStream")
  enableButtonStop("stream")
  var e = document.getElementById("resolutionStream")
  var resolution = e.options[e.selectedIndex].value;
  
  console.log("resolution");
  
  console.log(resolution);
  console.log(getResolution(resolution));

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("POST /start_stream");
        console.log(this.responseText);
      }
    }
  xhttp.open("POST", "/start_stream?id=" + userId, true);
  xhttp.send(getResolution(resolution));
  waitStartPreview()
}

function stopStream() {
  userId = getUrlParam('id', 'Empty')
  stopBlinking("blinkingStream")
  enableButtonStart("stream")
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("GET /stop_stream");
        console.log(this.responseText);
      }
    }
  xhttp.open("GET", "/stop_stream?id=" + userId, true);
  xhttp.send();

}

function waitStartPreview() {
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("GET /wait_start_preview");
        console.log(this.responseText);
        startPreview()
      }
    }
  xhttp.open("GET", "/wait_start_preview?id=" + userId, true);
  xhttp.send();
}

// ---------------------
// ---------Video-Record----------
function startRecord() {
  startBlinking("blinkingRecord")
  enableButtonStop("record")
  startStopWatch();
  document.getElementById("info").setAttribute("title", "Зупиніть запис відео")
  document.getElementById("videoResolution").setAttribute("disabled", "true")
  console.log("starting recording");

  var e = document.getElementById("resolutionRecord")
  var resolution = e.options[e.selectedIndex].value;
  
  console.log("resolution");
  
  console.log(resolution);
  console.log(getResolution(resolution));

  console.log(document.getElementById("start-record-input").value)
  var filename = document.getElementById("start-record-input").value
  userId = getUrlParam('id', 'Empty')

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("POST /start_record");
        console.log(this.responseText);
      }
    }
  xhttp.open("POST", "/start_record?id=" + userId, true);
  xhttp.send(filename);
}

function stopRecord() {
  stopBlinking("blinkingRecord");
  stopStopWatch();
  document.getElementById("info").removeAttribute("title")
  document.getElementById("videoResolution").removeAttribute("disabled")
  enableButtonStart("record")
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("GET /stop_record");
        console.log(this.responseText);
      }
    }
  xhttp.open("GET", "/stop_record?id=" + userId, true);
  xhttp.send();
}
// -----------------------
// --------settings-------
function getStreamSettings() {
  console.log("In settings");
  var xhttp = new XMLHttpRequest();
  var userId = getUrlParam('id', 'Empty')
  console.log(userId);
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var str = this.responseText;
      var replacedStr = str.replace(/'/g, "\"")
      var data = JSON.parse(replacedStr)
      console.log(data);

      document.getElementById("streamLink").value = data["youtube"];
      document.getElementById("streamKey").value = data["key"];

      // console.log(this.responseText);
    }
  }
  xhttp.open("GET", "/stream_settings?id=" + userId, true);
  xhttp.send();
}
// --------------------------