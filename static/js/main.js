// document.getElementById("TextBlock").innerHTML = 100;


loadDoc();
window.setInterval(function () {
   loadDoc()
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

  
}

var isBlocked = false;
function loadDoc() {
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
     
      var data = JSON.parse(this.responseText);
      
      switch (data["waterLevel"]) {
        case 20:
          document.getElementById('topWater').style.background = "green";
          break;
        case 40:
          document.getElementById('topWater').style.background = "purple";
          break;
        case 60:
          document.getElementById('topWater').style.background = "orange";
          break;
        case 80:
          document.getElementById('topWater').style.background = "blue";
          break;
        case 90:
          document.getElementById('topWater').style.background = "red";
          break;
      }
          // document.getElementById("topWater").style.background = "green"
          document.getElementById('sky').style.height = data["waterLevel"] + "%";
      data["sensors"].map(sensor => {
        
        document.getElementById(sensor.name + "Hum").innerHTML = sensor["Hum"] + " %";
        document.getElementById("humidityCircle" + sensor.name).setAttribute("stroke-dasharray", (sensor["Hum"] + " 135"));
        document.getElementById(sensor.name + "Temp").innerHTML = sensor["Temp"] + "&#8451";
        document.getElementById("tempCircle_" + sensor.name).setAttribute("style", '-webkit-transform: rotate(' +(sensor["Temp"] + 70) + 'deg);' )
      })

      if(data["connectedId"] != "0"){
        if (isBlocked == false && data["connectedId"] != userId && isPreviewStart == true){
          
          document.getElementById("start-stream").disabled = true;
          document.getElementById("capture-image").disabled = true;
          document.getElementById("start-record").disabled = true;
          isBlocked = true
        }
      }else {
        
        if (isPreviewStart == true && isBlocked == true) {
          console.log("Iin section remove disable");
          
          isBlocked = false
          document.getElementById("start-stream").removeAttribute("disabled")
          document.getElementById("capture-image").removeAttribute("disabled")
          document.getElementById("start-record").removeAttribute("disabled")
        }
      }
      
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

function getItemsTime(){
  
  var select = document.getElementById("inputInterval")
  select.innerHTML = ""
  for(let i = 1; i<= 10; i++){
    var option = document.createElement("option");
    option.innerHTML = i
    option.value = i
    select.appendChild(option)
  }
}

function setSettingsFeeder(){
  var userId = getUrlParam('id', 'Empty')
  var e = document.getElementById("inputInterval")
  var time = e.options[e.selectedIndex].value;

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange
    = function () {
      if (this.readyState == 4) {
        console.log("POST /set_settings_feeder");
        console.log(this.responseText);
      }
    }
  xhttp.open("POST", "/set_settings_feeder?id=" + userId, true);
  xhttp.send(time);
}

function feed(){
  var userId = getUrlParam('id', 'Empty')

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
        console.log("GET /feed");
        console.log(this.responseText);
      }
    }
  xhttp.open("GET", "/feed?id=" + userId, true);
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

// -------preview---------

function captureImage() {
  userId = getUrlParam('id', 'Empty')
  // enableButtonStart("preview")
  var xhttp = new XMLHttpRequest();
  var filename = document.getElementById("capture-input").value;
  var e = document.getElementById("resolutionImage")
  var resolution = e.options[e.selectedIndex].value;

  console.log("resolution");

  console.log(resolution);

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
  var result = {
    "filename": filename,
    "resolution": getResolution(resolution)
  }
  xhttp.send(JSON.stringify(result));
}





// -------------------
function getResolution(resolution) {
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
  var result = {
    "filename":filename,
    "resolution": getResolution(resolution)
  }
  xhttp.send(JSON.stringify(result));
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
      // var replacedStr = str.replace(/'/g, "\"")
      // var data = JSON.parse(replacedStr)
      var data = JSON.parse(str)
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
function setStreamSettings() {
  console.log("In set settings");
  var xhttp = new XMLHttpRequest();
  var userId = getUrlParam('id', 'Empty')
  console.log(userId);
  var youtube = document.getElementById("streamLink").value;
  var key = document.getElementById("streamKey").value;
  var result = {
    "youtube": youtube,
    "key": key
  }
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var str = this.responseText;
      // var replacedStr = str.replace(/'/g, "\"")
      // var data = JSON.parse(replacedStr)
      // var data = JSON.parse(str)
      // console.log(data);

      // document.getElementById("streamLink").value = data["youtube"];
      // document.getElementById("streamKey").value = data["key"];

      // console.log(this.responseText);
    }
  }
  xhttp.open("POST", "/set_stream_settings?id=" + userId, true);
  xhttp.send(JSON.stringify(result));
}