loadDoc()
window.setInterval(function () {
  loadDoc()
}, 5000)



function onFullScreen() {
  var fullScreen = document.getElementById("fullScreen");

  fullScreen.webkitRequestFullScreen()
  if (document.webkitFullscreenElement) {
    document.webkitCancelFullScreen();
    var image = document.getElementById("badge");
    image.setAttribute("width", "640")
    image.setAttribute("height", "480")
  }

  else {
    fullScreen.webkitRequestFullScreen();
    var image = document.getElementById("badge");
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

      document.getElementById('sky').style.height = data["waterLevel"] + "%";
      data["sensors"].map(sensor => {

        document.getElementById(sensor.name + "Hum").innerHTML = sensor["Hum"] + " %";
        document.getElementById("humidityCircle" + sensor.name).setAttribute("stroke-dasharray", (sensor["Hum"] + " 135"));
        document.getElementById(sensor.name + "Temp").innerHTML = sensor["Temp"] + "&#8451";
        document.getElementById("tempCircle_" + sensor.name).setAttribute("style", '-webkit-transform: rotate(' + (sensor["Temp"] + 70) + 'deg);')
      })

      if (data["streaming"] === true) {
        if (document.getElementById("start-stream").hasAttribute("disabled") != true) {
          enableButtonStop("stream")
          startBlinking("blinkingStream")

        }

      } else {
        if (document.getElementById("start-stream").hasAttribute("disabled")) {
          enableButtonStart("stream")
          stopBlinking("blinkingStream")

        }
      }

      if (data["connectedId"] != "0") {
        if (isBlocked == false && data["connectedId"] != userId && isPreviewStart == true) {

          document.getElementById("capture-image").disabled = true;
          document.getElementById("start-record").disabled = true;
          isBlocked = true
        }
      } else {

        if (isPreviewStart == true && isBlocked == true) {
          isBlocked = false
          document.getElementById("capture-image").removeAttribute("disabled")
          document.getElementById("start-record").removeAttribute("disabled")
        }
      }

    }
  }
  xhttp.open("GET", "/sensors", true);
  xhttp.send();
}

function shutdownPi() {
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/shutdown_pi?id=" + userId, true);
  xhttp.send();
}

function rebootPi() {
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/reboot_pi?id=" + userId, true);
  xhttp.send();
}


function onRefreshList() {
  setTimeout(function () {
    getVideoFiles();
  }
    , 2000);
}

function getExtensionFile(filename) {
  return filename.substring(filename.lastIndexOf('.') + 1, filename.length) || filename;
}

function getVideoFiles() {
  let userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var response = this.responseText;
      var data = response.substring(2, response.length - 2)
      var fileNames = data.split("', '");

      document.getElementById("fileList").innerHTML = "";

      if (fileNames != undefined && fileNames.length > 0 && fileNames[0] != "") {
        fileNames.forEach(file => {
          var a = document.createElement('a');
          a.className = "list-group-item list-group-item-action";
          a.innerHTML = file;

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
    }
  }
  xhttp.open("GET", "/media?id=" + userId, true);
  xhttp.send();
}

function getItemsTime() {

  var select = document.getElementById("inputInterval")
  select.innerHTML = ""
  for (let i = 1; i <= 10; i++) {
    var option = document.createElement("option");
    option.innerHTML = i
    option.value = i
    select.appendChild(option)
  }
}

function setSettingsFeeder() {
  var userId = getUrlParam('id', 'Empty')
  var e = document.getElementById("inputInterval")
  var time = e.options[e.selectedIndex].value;

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/set_settings_feeder?id=" + userId, true);
  xhttp.send(time);
}

function feed() {
  var userId = getUrlParam('id', 'Empty')

  var xhttp = new XMLHttpRequest();

  xhttp.open("GET", "/feed?id=" + userId, true);
  xhttp.send();
}

// ----------------------------------------

// -------preview---------

function captureImage() {
  var filename = document.getElementById("capture-input").value;
  if (filename.length > 0) {
    userId = getUrlParam('id', 'Empty')
    var xhttp = new XMLHttpRequest();

    var e = document.getElementById("resolutionImage")
    var resolution = e.options[e.selectedIndex].value;

    xhttp.onreadystatechange = function () {
      if (this.readyState == 4) {
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


        setTimeout(function () {
          document.getElementById("alertBlock").innerHTML = "";
        }, 5000);
      }
    }
    xhttp.open("POST", "/capture_image?id=" + userId, true);
    var result = {
      "filename": filename,
      "resolution": getResolution(resolution)
    }
    xhttp.send(JSON.stringify(result));
  }else{
    alert("Введіть ім'я зображення")
  }

}

// -------------------
function getResolution(resolution) {
  switch (resolution) {
    case "720":
      return "1280x720"
      break;

    case "480":
      return "854x480"
      break;

    case "240":
      return "426x240"
      break;
    default:
      break;
  }
}

// ---------------------
// ---------Video-Record----------
function startRecord() {
  var filename = document.getElementById("start-record-input").value
  if (filename.length > 0) {
    startBlinking("blinkingRecord")
    enableButtonStop("record")
    startStopWatch();
    document.getElementById("info").setAttribute("title", "Зупиніть запис відео")
    document.getElementById("videoResolution").setAttribute("disabled", "true")

    var e = document.getElementById("resolutionRecord")
    var resolution = e.options[e.selectedIndex].value;


    userId = getUrlParam('id', 'Empty')

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange
      = function () {
        if (this.readyState == 4) {
        }
      }
    xhttp.open("POST", "/start_record?id=" + userId, true);
    var result = {
      "filename": filename,
      "resolution": getResolution(resolution)
    }
    xhttp.send(JSON.stringify(result));
  } else {
    alert("Введіть ім'я відеофайлу")
  }

}

function stopRecord() {
  stopBlinking("blinkingRecord");
  stopStopWatch();
  document.getElementById("info").removeAttribute("title")
  document.getElementById("videoResolution").removeAttribute("disabled")
  enableButtonStart("record")
  userId = getUrlParam('id', 'Empty')
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/stop_record?id=" + userId, true);
  xhttp.send();
}
// -----------------------
// --------settings-------
function getStreamSettings() {
  var xhttp = new XMLHttpRequest();
  var userId = getUrlParam('id', 'Empty')
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var str = this.responseText;
      var data = JSON.parse(str)
      document.getElementById("streamLink").value = data["youtube"];
      document.getElementById("streamKey").value = data["key"];
    }
  }
  xhttp.open("GET", "/stream_settings?id=" + userId, true);
  xhttp.send();
}
// --------------------------

function setStreamSettings() {

  var userId = getUrlParam('id', 'Empty')
  var youtube = document.getElementById("streamLink").value;
  var key = document.getElementById("streamKey").value;
  if (youtube.length > 0 && key.length > 0) {
    var xhttp = new XMLHttpRequest();

    var result = {
      "youtube": youtube,
      "key": key
    }

    xhttp.open("POST", "/set_stream_settings?id=" + userId, true);
    xhttp.send(JSON.stringify(result));
  } else alert("Заповніть поля 'Посилання' та 'Ключ' ")
}