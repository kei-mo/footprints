//
function init() {
// Query with a new parameter 
    $.get("/init", function(data) {document.getElementById("plotimg").src = data;
    });
};
//
// Register Event handle
init();
