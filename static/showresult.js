
function showresult() {
    var result1;
    var result2;
    $.get("/show/result1", function(data){
        var result1 =  data;
    document.getElementById("result1").textContent = result1;
    });
    
    $.get("/show/result2", function(data){
    var result2 =  data;
    document.getElementById("result2").textContent = result2
    });

}

//
// Register Event handler

document.getElementById("plotimg").addEventListener("load", function(){
    showresult();
}, false);
