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