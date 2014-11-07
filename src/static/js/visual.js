$(document).ready(function() {
    onResize();
    $(window).resize(function() {
        onResize();
    });
});

function onResize() {
    var window_height = $(window).height();
    var window_width = $(window).width();

    /**
     adjustments related to height
    **/

    // adjust textarea height
    $('.code-pane').height(window_height-80);
}