document.getElementById("TextBlock").innerHTML = 100;


loadDoc();
window.setInterval(function(){
//  loadDoc()
}, 5000)

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

function loadDoc(){

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      var data = document.test_form.test_text.value;
        sensors = JSON.parse(this.responseText)
      console.log(data);
      document.getElementById("TextBlock").innerHTML = this.responseText ;
      document.getElementById("sotTemp").innerHTML = sensors[0][0] ;
      document.getElementById("sotHum").innerHTML = sensors[0][1] + "%";
      document.getElementById("humidityCircle").setAttribute("stroke-dasharray",(sensors[0][1] + " 135"));
      let sotHum = sensors[0][1];
      // document.getElementById("humAnimation").setAttribute("values",
      // ("0 200; " + ((sotHum/6) + " 180; ") + ((sotHum/4) + " 150; ") + ((sotHum/7) + " 135; ") + (sensors[0][1] + " 135; ")+(sensors[0][1] + " 135; ")));

      document.getElementById("arenaTemp").innerHTML = sensors[1][0] ;
      document.getElementById("arenaHum").innerHTML = sensors[1][1] ;
      document.getElementById("roomTemp").innerHTML = sensors[2][0] ;
      document.getElementById("roomHum").innerHTML = sensors[2][1] ;
// Water level
      switch(sensors[3]){
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
  xhttp.open("GET","/sensors", true);
  xhttp.send();
}

function makePOSTStart(){

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4) {

      console.log("POST");
      console.log(this.responseText);
      console.log(document.getElementById('badge').src)
      document.getElementById('badge').src = "http://192.168.1.37:8002/stream.mjpg";
    }
  }
  xhttp.open("POST","/start", true);
  xhttp.send(12);

}

function makePOSTStop(){

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4) {
      console.log("POST");
      console.log(this.responseText);
    }
  }
  xhttp.open("POST","/stop", true);
  xhttp.send(12);
}
