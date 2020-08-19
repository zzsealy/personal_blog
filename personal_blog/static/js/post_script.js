$(document).ready(function () {
    var segs = [];
    $("h2").each(function (index, node) {
        
        segs.push(node)
        
    });
    for(let i=0; i<segs.length;i++) {
        console.log($(segs[i]).children("a").html())
        var link = $("<a></a>").attr("href", "#" + $(segs[i]).children("a").html()).text($(segs[i]).children("a").html())
        if (!i) {
            link.addClass("active")
        }
        var row = $("<li></li>").append(link)
        $("#subtitle ul").append(row)
    }
})


