document.getElementById("TextBlock").innerHTML = 100;

console.log()
loadDoc();
window.setInterval(function(){
//  loadDoc()
}, 5000)

function loadDoc(){

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      var data = document.test_form.test_text.value;

      console.log(data);
      document.getElementById("TextBlock").innerHTML = this.responseText ;

      console.log("Response");
      console.log(this.responseText);
    }
  }
  xhttp.open("GET","/sensors", true);
  xhttp.send();
}

function makePOST(){

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if(this.readyState == 4) {

      console.log("POST");
      console.log(this.responseText);
    }
  }
  xhttp.open("POST","/send", true);
  xhttp.send(12);
}
