
    //
function plotcountry2(targetid) {

// Buid query parameter
    var param = {};
    //exp
    // form要素を取得
    var element = document.getElementById(targetid) ;
    // form要素内のラジオボタングループ(name="hoge")を取得
    var radioNodeList = element.experience ;
    // 選択状態の値(value)を取得 (Bが選択状態なら"b"が返る)
    var a = radioNodeList.value ;
    
    if ( a === "" ) {
        // 未選択状態
    } else {
        // aには選択状態の値が代入されている
        param["experience"] = a;
    };

    param["country"] = targetid;
    var query = jQuery.param(param);

// Query with a new parameter 
    $.get("/plot/country" + "?" + query, function(data) {
        document.getElementById("plotimg").src = data;
    });
};
    
//
// Register Event handler
//
var pages = document.getElementById('tabbody').getElementsByTagName('div');

for(var j=0; j<pages.length; j++) {
    // Pageごとに処理 
    pageid = pages[j].id;
    var cntIds = document.getElementById(pageid).getElementsByTagName('form');

    // 各ラジオボダンにイベントハンドラーを結びつける
    for(var i=0; i<cntIds.length; i++) {
        var targetid = cntIds[i].id
        // alert(targetid)
        document.getElementById(targetid).addEventListener("change", function(event){
            var targetid =  $(this).attr("id");
            plotcountry2(targetid);
        }, false);
    };
}
