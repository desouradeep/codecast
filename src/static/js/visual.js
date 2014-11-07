$(document).ready(function() {
    onResize();
    $(window).resize(function() {
        onResize();
    });
});

function onResize() {
    /**
    Redraw UI on resize, to remove posibilities of template breaking
    **/
    var window_height = $(window).height();
    var window_width = $(window).width();

    /**
     adjustments related to height
    **/

    // adjust textarea height
    $('.code-pane').height(window_height-80);
}

function loadPagelets(pagelets) {
    /**
    Send ajax requests to retrieve contents of every pagelet on the page
    **/
    for(var page in pagelets) {
        $.ajax({
            url: pagelets[page].url,
            async: false,
            success: function(result) {
                $('#' + pagelets[page].id).html(result);
            }
        });
    }
}
